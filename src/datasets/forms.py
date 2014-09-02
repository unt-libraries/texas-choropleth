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

    # Change the label of the published field.
    # This will change back in later versions
    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.fields['published'].label = 'Shared'

    class Meta:
        model = Dataset
        fields = ['name', 'description', 'label', 'published', 'license']

        # Add Bootstrap form classes to the widgets
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'published' : forms.Select(attrs={'class': 'form-control'}),
            'license': forms.Select(attrs={'class': 'form-control'}),
        }
