from rest_framework import serializers
from .models import Choropleth, Palette
# from datasets.models import Dataset, DatasetRecord
from datasets.serializers import DatasetSerializer


class ChoroplethSerializer(serializers.ModelSerializer):
    # dataset = DatasetSerializer()
    dataset = serializers.PrimaryKeyRelatedField()
    owner = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Choropleth
        fields = (
            'id',
            'name',
            'description',
            'published',
            'scheme',
            'palette',
            'data_classes',
            'dataset',
            'owner'
        )


class PaletteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palette
        fields = ('name', 'class_name')

class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choropleth
        fields = ('scheme')
