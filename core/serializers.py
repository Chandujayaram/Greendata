from rest_framework import serializers
from .models import DataSource, EmissionRecord

class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = '__all__'

class EmissionRecordSerializer(serializers.ModelSerializer):
    source_name = serializers.SerializerMethodField()
    source_type = serializers.SerializerMethodField()

    def get_source_name(self, obj):
        return obj.source.name if obj.source else 'N/A'

    def get_source_type(self, obj):
        return obj.source.source_type if obj.source else 'N/A'

    class Meta:
        model = EmissionRecord
        fields = '__all__'