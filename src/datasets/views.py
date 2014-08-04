from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from .models import Dataset
from .forms import DatasetUploadForm

class DatasetManagementView(ListView):
    template_name="datasets/dataset_management.html"
    model = Dataset

class DatasetDetailView(FormMixin, DetailView):
    template_name="datasets/dataset_detail.html"
    model = Dataset
    context_object_name = "dataset"
    form_class = DatasetUploadForm

    def get_context_data(self, **kwargs):
        context = super(DatasetDetailView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        return context
