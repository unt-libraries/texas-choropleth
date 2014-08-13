from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework import viewsets
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from .models import Choropleth, Palette
from .serializers import ChoroplethSerializer, PaletteSerializer
from datasets.serializers import DatasetSerializer
from datasets.models import Dataset

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


class ChoroplethDetail(DetailView):
    model = Choropleth
    template_name = 'choropleth/choropleth_detail.html'
    

class ChoroplethDetail(DetailView):
    template_name = 'choropleth/choropleth_view.html'
    model = Choropleth 


class ChoroplethCreate(TemplateView):
    template_name = "choropleth/choropleth_create.html"
    
    def get_context_data(self, **kwargs):
        context = super(ChoroplethCreate, self).get_context_data(**kwargs)
        context['dataset'] = Dataset.objects.get(id=kwargs['pk'])
        return context


class ChoroplethAPI(viewsets.ModelViewSet):
    model = Choropleth
    serializer_class = ChoroplethSerializer 
    
