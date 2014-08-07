from django.forms import ModelForm 
from .models import DatasetDocument, Dataset

class DatasetUploadForm(ModelForm):
    class Meta:
        model = DatasetDocument
        fields = ['datafile']
        labels = {
            'datafile': ('CSV File'),
        }

class DatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'description', 'license', 'scheme']
