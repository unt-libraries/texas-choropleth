from django.test import TestCase
from django.contrib.auth.models import User
from .models import Dataset, DatasetRecord, DatasetDocument
from cartograms.models import Cartogram
from django.core.files.base import File

class DatasetTestCase(TestCase):
    fixtures = ['texas.json']

    def setUp(self):
        user = User.objects.create(username="test")
        dataset = Dataset.objects.create(name="Test", cartogram_id=1)
        DatasetDocument.objects.create(
            owner = user,
            dataset = dataset,
            datafile = File(open('tmp/unemployment.csv'))
        )
        
    def test_import_dataset(self):
        dataset = Dataset.objects.get(name="Test")
        result = dataset.import_dataset()
        self.assertTrue(result)
        # check that the values exists

    def test_replace_imported_dataset(self):
        dataset =  Dataset.objects.get(name="Test")
        dataset.import_dataset() # Initial import

        # Import again to verify it can handle existant data
        result = dataset.import_dataset()
        self.assertFalse(result)
        # add validation that the object was updated

    def test_document_is_invalid(self):
        dataset = Dataset.objects.get(name="Test")
        document = dataset.get_datafile()
        dataset.validate_datafile()
