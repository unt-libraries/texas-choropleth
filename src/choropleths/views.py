import os
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from choropleth.settings import IMAGE_EXPORT_TMP_DIR
from rest_framework import generics
from rest_framework import viewsets
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.core.files.base import File
from .models import Choropleth, Palette
from .serializers import ChoroplethSerializer, PaletteSerializer
from datasets.serializers import DatasetSerializer
from datasets.models import Dataset
from .screenshot import get_screen_shot


class GetPublishedObjectMixin(object):
    """
    Get Object Mixin

    Retrieves the object if the request user is the owner, or if
    the object is published. Otherwise returns status 403
    """
    def get_object(self, **kwargs):
        gotten_object = super(GetPublishedObjectMixin, self).get_object(**kwargs)
        if gotten_object.owner != self.request.user:
            if gotten_object.published == 0:
                raise PermissionDenied()
        return gotten_object


class GalleryView(generic.ListView):
    model = Choropleth
    template_name = "choropleths/gallery.html"
    paginate_by = 12
    queryset = Choropleth.objects.filter(published=1).order_by('-created_at', 'name').select_related('dataset')


class ChoroplethExport(generic.DetailView):
    model = Choropleth
    template_name = "choropleths/choropleth_export.html"


class ChoroplethList(generic.ListView):
    model = Choropleth
    template_name = 'choropleths/choropleth_list.html'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.id)
        return Choropleth.objects.filter(owner=user).order_by('-modified_at').select_related('dataset')


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
        if obj.published:
            export = reverse('choropleths:choropleth-export', kwargs={'pk': obj.id})
            url = self.request.build_absolute_uri(export)

            filename = "{0}.png".format(obj.id)

            options = {
                'url': url,
                'filename': filename,
                'path': IMAGE_EXPORT_TMP_DIR,
                'crop': True,
                'crop_replace': False,
                'thumbnail': True,
                'thumbnail_replace': False,
                'thumbnail_width': 200,
                'thumbnail_height': 150
            }

            screen_path, crop_path, thumbnail_path = get_screen_shot(**options)

            f = File(open(thumbnail_path))
            obj.thumbnail = f
            obj.save()

            os.remove(screen_path)
            os.remove(crop_path)
            os.remove(thumbnail_path)



