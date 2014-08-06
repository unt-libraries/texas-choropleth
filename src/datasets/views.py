from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin
from .models import Dataset, DatasetDocument
from .forms import DatasetUploadForm

class DatasetManagement(ListView):
    template_name="datasets/dataset_management.html"
    model = Dataset


class DatasetDisplay(DetailView):
    model = Dataset

    def get_context_data(self, **kwargs):
        context = super(DatasetDisplay, self).get_context_data(**kwargs)
        context['form'] = DatasetUploadForm()
        return context


class DatasetUpload(SingleObjectMixin, FormView):
    template_name = 'datasets/dataset_detail.html'
    form_class = DatasetUploadForm
    model = Dataset

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DatasetUpload, self).post(request, *args, **kwargs)

    def get_form(self, form_class):
        if 0 != len(self.request.FILES):
            try:
                document = DatasetDocument.objects.get(dataset_id=self.object.pk)
                return form_class(instance=document, **self.get_form_kwargs())
            except DatasetDocument.DoesNotExist:
                return form_class(**self.get_form_kwargs())
        else:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        document = form.save(commit=False)
        document.dataset = self.object
        document.owner_id = 1 # change this once auth is in place
        document.save()
        self.object.import_dataset()
        return super(DatasetUpload, self).form_valid(form)

    def get_success_url(self):
        return reverse('datasets:dataset-detail', kwargs={'pk': self.object.pk})


class DatasetDetail(View):
    def get(self, request, *args, **kwargs):
        view = DatasetDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = DatasetUpload.as_view()
        return view(request, *args, **kwargs)

