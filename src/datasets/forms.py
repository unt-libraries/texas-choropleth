from django import forms 
from .models import DatasetDocument, Dataset

class DatasetUploadForm(forms.ModelForm):
    class Meta:
        model = DatasetDocument
        fields = ['datafile']
        labels = {
            'datafile': ('CSV File'),
        }

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'description', 'published', 'license']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'published' : forms.Select(attrs={'class': 'form-control'}),
            'license': forms.Select(attrs={'class': 'form-control'}),
        }
