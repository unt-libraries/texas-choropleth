from django.forms import ModelForm 
from .models import DatasetDocument

class DatasetUploadForm(ModelForm):
    class Meta:
        model = DatasetDocument
        fields = ['datafile']
