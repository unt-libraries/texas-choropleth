from rest_framework import serializers

from cartograms.models import Cartogram
from datasets.models import Dataset, DatasetRecord


class DatasetRecordNameField(serializers.Field):
    def field_to_native(self, obj, field_name):
        return obj.cartogram_entity.name


class DatasetRecordSerializer(serializers.ModelSerializer):
    cartogram_entity = serializers.SlugRelatedField(
        read_only=True,
        slug_field='entity_id')
    name = DatasetRecordNameField()

    class Meta:
        model = DatasetRecord
        fields = ('id', 'name', 'cartogram_entity', 'value')


class CartogramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cartogram
        fields = (
            'id',
            'name',
            'region_label',
            'subregion_label',
            'json_filename',
        )


class DatasetSerializer(serializers.ModelSerializer):
    records = DatasetRecordSerializer(many=True)
    cartogram = CartogramSerializer()
    domain = serializers.SerializerMethodField('get_domain')
    scale_options = serializers.SerializerMethodField('get_scales_options')

    class Meta:
        model = Dataset
        fields = (
            'id',
            'name',
            'label',
            'scale_options',
            'cartogram',
            'domain',
            'records',
        )

    def get_domain(self, obj):
        """
        Format the min and max into a dictionary for the JS to reference by key
        """

        return {
            'min': obj.min_record,
            'max': obj.max_record,
            'non_zero_min': obj.non_zero_min_record,
            'non_zero_max': obj.non_zero_max_record
        }

    def get_scales_options(self, obj):
        """
        Format the data into a dictionary for the JS to reference by key
        """
        scales = obj.get_scale_options()
        keys = ['id', 'name']

        return map(lambda scale: dict(zip(keys, scale)), scales)
