from django.test import TestCase
from django.core.urlresolvers import reverse
from datasets.models import Dataset, DatasetRecord
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Choropleth

from model_mommy import mommy
from model_mommy.recipe import seq


class ChoroplethTestCase(TestCase):

    def setUp(self):
        self.dataset = mommy.make(Dataset)
        records = mommy.make(DatasetRecord, _quantity=10, value=seq(0))
        for record in records:
            self.dataset.records.add(record)
        self.choropleth = mommy.make(Choropleth, dataset=self.dataset)

    def test_has_records_is_true(self):
        self.assertTrue(self.choropleth.has_records())

    def test_has_records_is_false(self):
        choropleth = mommy.make(
                Choropleth,
                dataset=mommy.make(Dataset))
        self.assertFalse(choropleth.has_records())

    def test_has_records_is_false_without_dataset(self):
        choropleth = mommy.make(Choropleth)
        self.assertFalse(choropleth.has_records())

    def test_get_dataset_id(self):
        self.assertTrue(self.choropleth.get_dataset_id())

    def test_get_dataset_id_without_dataset(self):
        choropleth = mommy.make(Choropleth)
        self.assertFalse(choropleth.get_dataset_id())


class ChoroplethViewsTestCase(TestCase):
    def setUp(self):
        self.user1 = mommy.make(User, password=make_password('password'))
        self.user2 = mommy.make(User, password=make_password('password'))
        self.dataset = mommy.make(Dataset, owner=self.user1)
        self.choropleth = mommy.make(Choropleth, dataset=self.dataset, owner=self.user1)

    def test_anon_user_can_view_choropleth_list(self):
        response = self.client.get(reverse('choropleths:list'))
        self.assertEqual(response.status_code, 302)

    def test_user_can_view_choropleth_list(self):
        self.client.login(username=self.user1.username, password='password')
        response = self.client.get(reverse('choropleths:list'))
        self.assertEqual(response.status_code, 200)

    def test_non_owner_cannot_view_choropleth_detail(self):
        self.client.login(username=self.user2.username, password='password')
        response = self.client.get(reverse(
            'choropleths:detail',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 403)

    def test_non_owner_can_view_choropleth_detail(self):
        self.choropleth.published = 1
        self.choropleth.save()
        self.client.login(username=self.user2.username, password='password')
        response = self.client.get(reverse(
            'choropleths:detail',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 200)

    def test_anon_user_cannot_view_choropleth_create(self):
        response = self.client.get(reverse(
            'choropleths:create',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 302)

    def test_non_owner_cannot_view_choropleth_create(self):
        self.client.login(username=self.user2.username, password='password')
        response = self.client.get(reverse(
            'choropleths:create',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_view_choropleth_create(self):
        self.client.login(username=self.user1.username, password='password')
        response = self.client.get(reverse(
            'choropleths:create',
            args=[self.dataset.id]))
        self.assertEqual(response.status_code, 200)

    def test_anon_user_cannot_view_choropleth_edit(self):
        response = self.client.get(reverse(
            'choropleths:edit',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 302)

    def test_non_owner_cannot_view_choropleth_edit(self):
        self.client.login(username=self.user2.username, password='password')
        response = self.client.get(reverse(
            'choropleths:edit',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_view_choropleth_edit(self):
        self.client.login(username=self.user1.username, password='password')
        response = self.client.get(reverse(
            'choropleths:edit',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 200)

    def test_anon_user_can_view_choropleth_view_when_published(self):
        self.choropleth.published = 1
        self.choropleth.save()
        response = self.client.get(reverse(
            'choropleths:view',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 200)

    def test_non_owner_can_view_choropleth_view_when_published(self):
        self.client.login(username=self.user2.username, password='password')
        self.choropleth.published = 1
        self.choropleth.save()
        response = self.client.get(reverse(
            'choropleths:view',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 200)

    def test_owner_can_view_choropleth_view_when_published(self):
        self.client.login(username=self.user2.username, password='password')
        self.choropleth.published = 1
        self.choropleth.save()
        response = self.client.get(reverse(
            'choropleths:view',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 200)

    def test_anon_user_cannot_view_choropleth_view_when_not_published(self):
        response = self.client.get(reverse(
            'choropleths:view',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 403)

    def test_non_owner_cannot_view_choropleth_view_when_not_published(self):
        self.client.login(username=self.user2.username, password='password')
        response = self.client.get(reverse(
            'choropleths:view',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_view_choropleth_view_when_not_published(self):
        self.client.login(username=self.user2.username, password='password')
        self.choropleth.published = 1
        self.choropleth.save()
        response = self.client.get(reverse(
            'choropleths:view',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 200)

    def test_choropleth_export(self):
        response = self.client.get(reverse(
            'choropleths:export',
            args=[self.choropleth.id]))
        self.assertEqual(response.status_code, 200)
