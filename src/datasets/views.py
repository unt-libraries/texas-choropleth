from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.views import generic
from rest_framework.generics import RetrieveAPIView
from .models import Dataset, DatasetDocument
from .serializers import DatasetSerializer
from .forms import DatasetUploadForm, DatasetForm

class IndexView(generic.TemplateView):
    template_name = 'datasets/index.html'


class DatasetManagement(generic.ListView):
    template_name="datasets/dataset_management.html"
    model = Dataset

    def get_queryset(self):
        return Dataset.objects.filter(owner_id=self.request.user.pk)


class DatasetDisplay(generic.DetailView):
    model = Dataset

    def get_context_data(self, **kwargs):
        context = super(DatasetDisplay, self).get_context_data(**kwargs)
        context['form'] = DatasetUploadForm()
        return context

    def get_object(self, **kwargs):
        dataset = super(DatasetDisplay, self).get_object(**kwargs)
        if dataset.owner != self.request.user:
            raise PermissionDenied()
        else:
            return dataset


class DatasetUpload(generic.detail.SingleObjectMixin, generic.FormView):
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
        document.owner = self.request.user 
        document.save()
        self.object.import_dataset()
        return super(DatasetUpload, self).form_valid(form)

    def get_success_url(self):
        return reverse('datasets:dataset-detail', kwargs={'pk': self.object.pk})


class DatasetDetail(generic.View):
    def get(self, request, *args, **kwargs):
        view = DatasetDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = DatasetUpload.as_view()
        return view(request, *args, **kwargs)


class DatasetCreate(generic.edit.CreateView):
    template_name = 'datasets/dataset_create.html'
    model = Dataset
    form_class = DatasetForm

    def form_valid(self, form):
        dataset = form.save(commit=False)
        dataset.cartogram_id = 1 

        dataset.owner = self.request.user# change this once auth is in place
        dataset.save()
        return super(DatasetCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('datasets:dataset-detail', kwargs={'pk': self.object.pk})

class DatasetAPIView(RetrieveAPIView):
    model = Dataset 
    serializer_class = DatasetSerializer
