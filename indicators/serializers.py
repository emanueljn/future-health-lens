from rest_framework import serializers
from .models import IndicatorValue

class IndicatorValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorValue
        fields = "__all__"

class ForecastSerializer(serializers.Serializer):
    indicator = serializers.CharField()
    year = serializers.IntegerField()
    country = serializers.CharField()
    value = serializers.FloatField()
    source = serializers.CharField(default="Predicted by LinearRegression", read_only=True)