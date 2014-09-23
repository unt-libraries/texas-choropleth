import csv

from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views import generic
from rest_framework.generics import RetrieveAPIView
from .models import Dataset, DatasetDocument
from .serializers import DatasetSerializer
from .forms import DatasetUploadForm, DatasetForm
from django.http import HttpResponse
from choropleths.views import GetPublishedObjectMixin, ListSortMixin


class DatasetManagement(ListSortMixin, generic.ListView):
    template_name = "datasets/dataset_management.html"
    model = Dataset
    paginate_by = 10

    def get_queryset(self):
        return self.get_sorted_queryset() \
            .filter(owner=self.request.user) \
            .select_related('choropleth')


class DatasetDisplay(GetPublishedObjectMixin, generic.DetailView):
    model = Dataset
    queryset = Dataset.objects.prefetch_related('records__cartogram_entity')

    def get_context_data(self, **kwargs):
        context = super(DatasetDisplay, self).get_context_data(**kwargs)
        context['form'] = DatasetUploadForm()
        return context


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
                document = DatasetDocument.objects \
                    .get(dataset_id=self.object.pk)

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
        return reverse(
            'datasets:dataset-detail',
            kwargs={'pk': self.object.pk})


class DatasetDetail(generic.View):
    def get(self, request, *args, **kwargs):
        view = DatasetDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = DatasetUpload.as_view()
        return view(request, *args, **kwargs)


class DatasetCreate(generic.edit.CreateView):
    template_name = 'datasets/dataset_edit.html'
    model = Dataset
    form_class = DatasetForm

    def form_valid(self, form):
        dataset = form.save(commit=False)
        dataset.cartogram_id = 1

        dataset.owner = self.request.user
        dataset.save()
        return super(DatasetCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            'datasets:dataset-detail',
            kwargs={'pk': self.object.pk})


class DatasetDelete(generic.edit.DeleteView):
    model = Dataset
    success_url = reverse_lazy('datasets:dataset-management')

    def delete(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            raise PermissionDenied
        return super(DatasetDelete, self).delete(request, *args, **kwargs)


class DatasetUpdate(generic.edit.UpdateView):
    template_name = 'datasets/dataset_edit.html'
    model = Dataset
    form_class = DatasetForm

    def get_success_url(self):
        return reverse(
            'datasets:dataset-detail',
            kwargs={'pk': self.object.pk})

    def get_object(self, **kwargs):
        dataset = super(DatasetUpdate, self).get_object(**kwargs)
        if dataset.owner != self.request.user:
            raise PermissionDenied()
        return dataset


class DatasetAPIView(RetrieveAPIView):
    model = Dataset
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.prefetch_related('records__cartogram_entity')


def export_dataset(request, pk):
    dataset = Dataset.objects.get(id=pk)
    if dataset.owner != request.user:
        raise PermissionDenied()

    fn = dataset.name.lower()
    content_disposition = 'attachment; filename="{}.csv"'.format(fn)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition

    writer = csv.writer(response)
    writer.writerow(['fips', 'name', 'value'])
    for record in dataset.records.all().order_by('cartogram_entity__entity_id'):
        if record.value is not None:
            writer.writerow([
                record.get_entity_id(),
                record.get_entity_name(),
                record.value.normalize()
                ])
        else:
            writer.writerow([record.get_entity_id(), record.get_entity_name(), ])

    return response
