from rest_framework import serializers
from django.db.models import Min, Max
from .models import Dataset, DatasetRecord

class DatasetRecordSerializer(serializers.ModelSerializer):
    cartogram_entity = serializers.SlugRelatedField(read_only=True, slug_field='entity_id')
    # cartogram_entity = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = DatasetRecord
        fields = ('id', 'cartogram_entity', 'value')


class DatasetSerializer(serializers.ModelSerializer):
    records = DatasetRecordSerializer(many=True)
    cartogram = serializers.PrimaryKeyRelatedField()
    domain = serializers.SerializerMethodField('get_domain')

    class Meta:
        model = Dataset
        fields = ('id','cartogram', 'domain', 'records')

    def get_domain(self, obj):
        return {'min': obj.get_min_record(), 'max': obj.get_max_record()}



