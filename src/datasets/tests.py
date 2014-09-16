from django.test import TestCase
from django.contrib.auth.models import User
from .models import Dataset, DatasetRecord, DatasetDocument
from .validators import import_validator, MESSAGES
from cartograms.models import Cartogram
from django.core.files.base import File
from django.core.exceptions import ValidationError

class ImportDatasetTestCase(TestCase):
    fixtures = ['texas.json']

    def setUp(self):
        user = User.objects.create(username="test")
        dataset = Dataset.objects.create(name="Test", cartogram_id=1)
        DatasetDocument.objects.create(
            owner = user,
            dataset = dataset,
            datafile = File(open('tmp/import_dataset1.csv'))
        )
        
    def test_import_dataset(self):
        dataset = Dataset.objects.get(name="Test")
        imported_records = dataset.import_dataset()
        self.assertEqual(imported_records['created'], 254)

    def test_no_records_updated(self):
        dataset =  Dataset.objects.get(name="Test")
        dataset.import_dataset() # Initial import

        # Import again to verify it can handle existant data
        imported_records = dataset.import_dataset()
        self.assertEqual(imported_records['updated'], 0)
        self.assertEqual(imported_records['created'], 0)

    def test_two_records_updated(self):
        dataset =  Dataset.objects.get(name="Test")

        # import the initial datafile
        dataset.import_dataset()

        # Attach a slightly different datafile and reimport
        dataset.document.datafile = File(open('tmp/import_dataset2.csv'))
        dataset.save()
        imported_records = dataset.import_dataset()

        self.assertEqual(imported_records['updated'], 2)


class DatasetValidatorTestCase(TestCase):
    fixtures = ['texas.json']

    def test_validator_fails_incorrect_delimiter(self):
        doc = File(open('tmp/unemployment.tsv'))
        with self.assertRaises(ValidationError) as cm:
            import_validator(doc)

        self.assertEqual(cm.exception.message, MESSAGES[0])

    def test_validator_fails_without_csv(self):
        doc = File(open('tmp/data.zip'))
        with self.assertRaises(ValidationError) as cm:
            import_validator(doc)

        self.assertEqual(cm.exception.message, MESSAGES[1])

    def test_validator_fails_without_headers(self):
        doc = File(open('tmp/unemployment.csv'))
        with self.assertRaises(ValidationError) as cm:
            import_validator(doc)

        self.assertTrue(MESSAGES[3][0:17] in cm.exception.message)

    def test_validator_fails_with_incorrect_entity_ids(self):
        doc = File(open('tmp/incorrect_entity_id.csv'))
        with self.assertRaises(ValidationError) as cm:
            import_validator(doc)

        self.assertTrue(MESSAGES[2][0:9] in cm.exception.message)

    def test_validator_fails_without_required_fields(self):
        doc = File(open('tmp/missing_value.csv'))
        with self.assertRaises(ValidationError) as cm:
            import_validator(doc)

        self.assertTrue(MESSAGES[4][0:20] in cm.exception.message)

    def test_validator_with_empty_rows(self):
        doc = File(open('tmp/missing_rows.csv'))
        self.assertTrue(import_validator(doc))
