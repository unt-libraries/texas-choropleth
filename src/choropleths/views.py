from django.views import generic
from django.core.exceptions import PermissionDenied
from datasets.models import Dataset

from core.views import ListSortMixin, GetPublishedObjectMixin
from .models import Choropleth


class ChoroplethExport(generic.DetailView):
    model = Choropleth
    template_name = "choropleths/choropleth_export.html"


class ChoroplethList(ListSortMixin, generic.ListView):
    model = Choropleth
    template_name = 'choropleths/choropleth_list.html'
    paginate_by = 10

    def get_queryset(self):
        return self.get_sorted_queryset() \
            .filter(owner=self.request.user) \
            .select_related('dataset')


class ChoroplethDetail(GetPublishedObjectMixin, generic.DetailView):
    model = Choropleth
    template_name = 'choropleths/choropleth_detail.html'


class ChoroplethView(GetPublishedObjectMixin, generic.DetailView):
    template_name = 'choropleths/choropleth_view.html'
    model = Choropleth


class ChoroplethEdit(GetPublishedObjectMixin, generic.DetailView):
    template_name = "choropleths/choropleth_edit.html"
    model = Choropleth

    def get_object(self, **kwargs):
        """
        Only the owner will get a status 200
        """
        choropleth = super(ChoroplethEdit, self).get_object(**kwargs)
        if choropleth.owner != self.request.user:
            raise PermissionDenied()
        return choropleth


class ChoroplethCreate(generic.TemplateView):
    template_name = "choropleths/choropleth_create.html"

    def get_context_data(self, **kwargs):
        context = super(ChoroplethCreate, self).get_context_data(**kwargs)
        dataset = Dataset.objects.get(id=kwargs['pk'])
        if dataset.owner == self.request.user:
            context['object'] = dataset
            context['dataset'] = dataset
            return context
        else:
            raise PermissionDenied()
