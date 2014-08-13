from rest_framework import serializers
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

    class Meta:
        model = Dataset
        fields = ('id','cartogram', 'records')


