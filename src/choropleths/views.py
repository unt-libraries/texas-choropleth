import os
from django.core.urlresolvers import reverse
from django.conf import settings
from rest_framework import generics
from rest_framework import viewsets
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.core.files.base import File
from datasets.models import Dataset

from core.views import ListSortMixin, GetPublishedObjectMixin
from .models import Choropleth, Palette
from .serializers import ChoroplethSerializer, PaletteSerializer
from .screenshot import get_screen_shot


class GalleryView(ListSortMixin, generic.ListView):
    model = Choropleth
    template_name = "choropleths/gallery.html"
    paginate_by = 12

    def get_queryset(self):
        return self.get_sorted_queryset() \
            .filter(published=1) \
            .select_related('dataset')


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


class PaletteAPIView(generics.ListAPIView):
    model = Palette
    serializer_class = PaletteSerializer

    def get_queryset(self):
        palettes = Palette.objects.filter(scheme=self.kwargs['pk'])
        return palettes


class ChoroplethAPI(viewsets.ModelViewSet):
    model = Choropleth
    serializer_class = ChoroplethSerializer 
    queryset = Choropleth.objects.select_related('dataset', 'palette')
    
    def pre_save(self, obj):
        obj.owner = self.request.user

    def post_save(self, obj, **kwargs):
        export = reverse('choropleths:choropleth-export', kwargs={'pk': obj.id})
        url = self.request.build_absolute_uri(export)

        filename = "{0}.png".format(obj.id)

        options = {
            'url': url,
            'filename': filename,
            'path': settings.IMAGE_EXPORT_TMP_DIR,
            'crop': True,
            'crop_replace': False,
            'thumbnail': True,
            'thumbnail_replace': False,
            'thumbnail_width': 200,
            'thumbnail_height': 150
        }

        screen_path, crop_path, thumbnail_path = get_screen_shot(**options)

        f = File(open(thumbnail_path))
        if obj.thumbnail:
            obj.thumbnail.delete()
        obj.thumbnail = f
        obj.save()

        os.remove(screen_path)
        os.remove(crop_path)
        os.remove(thumbnail_path)
