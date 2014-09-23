from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Dataset, DatasetRecord, DatasetDocument, SCALE_CHOICES
from .validators import import_validator, MESSAGES
from django.core.files.base import File
from django.core.exceptions import ValidationError

from model_mommy import mommy
from model_mommy.recipe import seq


class ImportDatasetTestCase(TestCase):
    """
    Test Case for import_dataset method
    """
    fixtures = ['texas.json']

    def setUp(self):
        user = User.objects.create(username="test")
        dataset = Dataset.objects.create(name="Test", cartogram_id=1)
        DatasetDocument.objects.create(
            owner=user,
            dataset=dataset,
            datafile=File(open('src/datasets/test_data/import_dataset1.csv'))
        )

    def test_import_dataset(self):
        dataset = Dataset.objects.get(name="Test")
        imported_records = dataset.import_dataset()
        self.assertEqual(imported_records['created'], 254)

    def test_no_records_updated(self):
        dataset = Dataset.objects.get(name="Test")
        dataset.import_dataset()  # Initial import

        # Import again to verify it can handle existant data
        imported_records = dataset.import_dataset()
        self.assertEqual(imported_records['updated'], 0)
        self.assertEqual(imported_records['created'], 0)

    def test_two_records_updated(self):
        dataset = Dataset.objects.get(name="Test")

        # import the initial datafile
        dataset.import_dataset()

        # Attach a slightly different datafile and reimport
        dataset.document.datafile = File(open('src/datasets/test_data/import_dataset2.csv'))
        dataset.save()
        imported_records = dataset.import_dataset()

        self.assertEqual(imported_records['updated'], 2)


class DatasetValidatorTestCase(TestCase):
    """
     Test Case for update validator
    """
    fixtures = ['texas.json']

    def test_validator_fails_incorrect_delimiter(self):
        doc = File(open('src/datasets/test_data/unemployment.tsv'))
        with self.assertRaises(ValidationError) as cm:
            import_validator(doc)

        self.assertEqual(cm.exception.message, MESSAGES[0])

    def test_validator_fails_without_csv(self):
        doc = File(open('src/datasets/test_data/data.zip'))
        with self.assertRaises(ValidationError) as cm:
            import_validator(doc)

        self.assertEqual(cm.exception.message, MESSAGES[1])

    def test_validator_fails_without_headers(self):
        doc = File(open('src/datasets/test_data/unemployment.csv'))
        with self.assertRaises(ValidationError) as cm:
            import_validator(doc)

        self.assertTrue(MESSAGES[3][0:17] in cm.exception.message)

    def test_validator_fails_with_incorrect_entity_ids(self):
        doc = File(open('src/datasets/test_data/incorrect_entity_id.csv'))
        with self.assertRaises(ValidationError) as cm:
            import_validator(doc)

        self.assertTrue(MESSAGES[2][0:9] in cm.exception.message)

    def test_validator_fails_without_required_fields(self):
        doc = File(open('src/datasets/test_data/missing_value.csv'))
        with self.assertRaises(ValidationError) as cm:
            import_validator(doc)

        self.assertTrue(MESSAGES[4][0:20] in cm.exception.message)

    def test_validator_with_empty_rows(self):
        doc = File(open('src/datasets/test_data/missing_rows.csv'))
        self.assertTrue(import_validator(doc))


class DatasetTestCase(TestCase):
    def setUp(self):
        self.dataset = mommy.make(Dataset)
        records = mommy.make(DatasetRecord, _quantity=10, value=seq(0))
        for record in records:
            self.dataset.records.add(record)

    def test_has_choropleth_is_false(self):
        # dataset = Dataset.objects.get(name="Test")
        self.assertFalse(self.dataset.has_choropleth())

    def test_has_choropleth_is_true(self):
        mommy.make('choropleths.Choropleth', dataset=self.dataset)
        self.assertTrue(self.dataset.has_choropleth())

    def test_has_records_is_false(self):
        dataset = mommy.make(Dataset)
        self.assertFalse(dataset.has_records())

    def test_has_records_is_true(self):
        self.assertTrue(self.dataset.has_records())

    def test_get_min_record(self):
        min_record = self.dataset.get_min_record()
        self.assertEqual(int(min_record), 1)

    def test_get_max_record(self):
        max_record = self.dataset.get_max_record()
        self.assertEqual(int(max_record), 10)

    def test_get_non_zero_min_record(self):
        self.dataset.records.add(mommy.make(DatasetRecord, value=0))
        min_record = self.dataset.get_min_record()
        non_zero_min_record = self.dataset.get_non_zero_min_record()
        self.assertEqual(int(min_record), 0)
        self.assertEqual(int(non_zero_min_record), 1)

    def test_get_non_zero_max_record(self):
        self.dataset = mommy.make(Dataset)
        value_seq = seq(1, increment_by=-1)
        records = mommy.make(DatasetRecord, _quantity=10, value=value_seq)
        for record in records:
            self.dataset.records.add(record)
        max_record = self.dataset.get_max_record()
        non_zero_max_record = self.dataset.get_non_zero_max_record()
        self.assertEqual(int(max_record), 0)
        self.assertEqual(int(non_zero_max_record), -1)

    def test_domain_contains_zero(self):
        self.dataset.records.add(mommy.make(DatasetRecord, value=0))
        self.assertTrue(self.dataset.domain_contains_zero())

    def test_domain_does_not_contains_zero(self):
        self.assertFalse(self.dataset.domain_contains_zero())

    def test_logarithmic_in_get_scale_options(self):
        scales = self.dataset.get_scale_options()
        self.assertIn(SCALE_CHOICES[0], scales)
        self.assertIn(SCALE_CHOICES[1], scales)

    def test_logarithmic_not_in_get_scale_options(self):
        self.dataset = mommy.make(Dataset)
        records = mommy.make(DatasetRecord, _quantity=10, value=seq(-5))
        for record in records:
            self.dataset.records.add(record)
        scales = self.dataset.get_scale_options()
        self.assertIn(SCALE_CHOICES[0], scales)
        self.assertNotIn(SCALE_CHOICES[1], scales)


class DatasetViewsTestCase(TestCase):
    def setUp(self):
        self.user1 = mommy.make(User, password=make_password('password'))
        self.user2 = mommy.make(User, password=make_password('password'))
        self.dataset = mommy.make(Dataset, owner=self.user1)

    def test_anon_user_cannot_view_dataset_management(self):
        response = self.client.get(reverse('datasets:dataset-management'))
        self.assertEqual(response.status_code, 302)

    def test_user_can_view_dataset_management(self):
        self.client.login(username=self.user1.username, password='password')
        response = self.client.get(reverse('datasets:dataset-management'))
        self.assertEqual(response.status_code, 200)

    def test_anon_user_cannot_view_dataset_detail(self):
        response = self.client.get(reverse(
            'datasets:dataset-detail',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 403)

    def test_non_owner_cannot_view_dataset_detail(self):
        self.client.login(username=self.user2.username, password='password')
        response = self.client.get(reverse(
            'datasets:dataset-detail',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_view_dataset_detail(self):
        self.client.login(username=self.user1.username, password='password')
        response = self.client.get(reverse(
            'datasets:dataset-detail',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 200)

    def test_anon_user_cannot_view_dataset_create(self):
        response = self.client.get(reverse('datasets:dataset-create'))
        self.assertEqual(response.status_code, 302)

    def test_view_dataset_create(self):
        self.client.login(username=self.user1.username, password='password')
        response = self.client.get(reverse('datasets:dataset-create'))
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_view_dataset_update(self):
        self.client.login(username=self.user2.username, password='password')
        response = self.client.get(reverse(
            'datasets:dataset-update',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_view_dataset_update(self):
        self.client.login(username=self.user1.username, password='password')
        response = self.client.get(reverse(
            'datasets:dataset-update',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 200)

    def test_anon_user_cannot_view_dataset_update(self):
        response = self.client.get(reverse(
            'datasets:dataset-update',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 302)

    def test_non_owner_cannot_view_dataset_export(self):
        self.client.login(username=self.user2.username, password='password')
        response = self.client.get(reverse(
            'datasets:dataset-export',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_view_dataset_export(self):
        self.client.login(username=self.user1.username, password='password')
        response = self.client.get(reverse(
            'datasets:dataset-export',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 200)

    def test_anon_user_cannot_view_dataset_export(self):
        response = self.client.get(reverse(
            'datasets:dataset-export',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 302)
