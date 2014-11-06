import os

from django.conf import settings
from django.core.files.base import File
from django.core.urlresolvers import reverse
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .serializers import ChoroplethSerializer, PaletteSerializer
from core.api.permissions import IsOwnerOrSafeMethods
from choropleths.screenshot import get_screen_shot
from choropleths.models import Choropleth, Palette


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
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsOwnerOrSafeMethods,)

    def pre_save(self, obj):
        obj.owner = self.request.user

    def post_save(self, obj, **kwargs):
        export = reverse(
            'choropleths:export',
            kwargs={'pk': obj.id})
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
