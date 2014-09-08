from rest_framework import serializers
from django.db.models import Min, Max
from .models import Dataset, DatasetRecord

class DatasetRecordNameField(serializers.Field):
    def field_to_native(self, obj, field_name):
        return obj.cartogram_entity.name


class DatasetRecordSerializer(serializers.ModelSerializer):
    cartogram_entity = serializers.SlugRelatedField(read_only=True, slug_field='entity_id')
    name = DatasetRecordNameField()
    value = serializers.SerializerMethodField('normalize_value')

    class Meta:
        model = DatasetRecord
        fields = ('id', 'name', 'cartogram_entity', 'value')

    def normalize_value(self, obj):
        """
        Convert to float to avoid extra processing client side.
        """
        if obj.value:
            return float(obj.value)


class DatasetSerializer(serializers.ModelSerializer):
    records = DatasetRecordSerializer(many=True)
    cartogram = serializers.PrimaryKeyRelatedField()
    domain = serializers.SerializerMethodField('get_domain')

    class Meta:
        model = Dataset
        fields = ('id', 'name','label', 'cartogram', 'domain', 'records')

    def get_domain(self, obj):
        return {'min': obj.get_min_record(), 'max': obj.get_max_record()}

