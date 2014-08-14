from django.shortcuts import render, get_object_or_404
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework import viewsets
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .models import Choropleth, Palette
from .serializers import ChoroplethSerializer, PaletteSerializer
from datasets.serializers import DatasetSerializer
from datasets.models import Dataset

class GalleryView(ListView):
    model = Choropleth
    template_name = "choropleth/gallery.html"
    queryset = Choropleth.objects.filter(published=1)

class ChoroplethAPIView(RetrieveAPIView):
    model = Choropleth
    serializer_class = ChoroplethSerializer


class PaletteAPIView(ListAPIView):
    model = Palette
    serializer_class = PaletteSerializer

    def get_queryset(self):
        palettes = Palette.objects.filter(scheme=self.kwargs['pk'])
        return palettes


class ChoroplethList(ListView):
    model = Choropleth
    template_name = 'choropleth/choropleth_list.html'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.id)
        return Choropleth.objects.filter(owner=user)


class ChoroplethDetail(DetailView):
    model = Choropleth
    template_name = 'choropleth/choropleth_detail.html'

    def get_object(self, **kwargs):
        choropleth = super(ChoroplethDetail, self).get_object(**kwargs)
        if choropleth.owner != self.request.user:
            raise PermissionDenied()
        return choropleth
    

class ChoroplethView(DetailView):
    template_name = 'choropleth/choropleth_view.html'
    model = Choropleth 

    def get_object(self, **kwargs):
        choropleth = super(ChoroplethView, self).get_object(**kwargs)
        if choropleth.owner != self.request.user:
            if choropleth.published == 0:
                raise PermissionDenied()
        return choropleth


class ChoroplethCreate(TemplateView):
    template_name = "choropleth/choropleth_create.html"
    
    def get_context_data(self, **kwargs):
        context = super(ChoroplethCreate, self).get_context_data(**kwargs)
        context['dataset'] = Dataset.objects.get(id=kwargs['pk'])
        return context


class ChoroplethAPI(viewsets.ModelViewSet):
    model = Choropleth
    serializer_class = ChoroplethSerializer 
    
    def pre_save(self, obj):
        obj.owner = self.request.user
