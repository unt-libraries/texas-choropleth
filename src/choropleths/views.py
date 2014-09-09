from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .models import Choropleth, Palette
from .serializers import ChoroplethSerializer, PaletteSerializer
from datasets.serializers import DatasetSerializer
from datasets.models import Dataset


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
    paginate_by = 10
    queryset = Choropleth.objects.filter(published=1).order_by('-created_at', 'name')


class ChoroplethList(generic.ListView):
    model = Choropleth
    template_name = 'choropleths/choropleth_list.html'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.id)
        return Choropleth.objects.filter(owner=user).order_by('-modified_at')


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
        Only the owner may show get a status 200
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
    
    def pre_save(self, obj):
        obj.owner = self.request.user
