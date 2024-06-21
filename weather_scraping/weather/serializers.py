from django.utils import timezone
from rest_framework import serializers
from weather.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ['date', 'temperature', 'weather_description']


class UpdateTimeSerializer(serializers.Serializer):
    new_time = serializers.DateTimeField()

    def validate_new_time(self, value):
        """ User can not set time less than current. """
        if value <= timezone.now():
            raise serializers.ValidationError("The time should be longer than the current time.")
        return value
