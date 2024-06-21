from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from weather.business_logic import perform_weather_scraping, set_new_time
from weather.models import Weather
from weather.serializers import WeatherSerializer, UpdateTimeSerializer


class WeatherView(generics.ListAPIView):
    """Show first 5 records from db"""
    queryset = Weather.objects.all().order_by('-id')[:6]
    serializer_class = WeatherSerializer


class UpdaterWeatherView(generics.ListAPIView):
    """run perform_weather_scraping immediately"""
    queryset = Weather.objects.all()

    def get(self, request, *args, **kwargs):
        list_weather_data = perform_weather_scraping()
        if isinstance(list_weather_data, dict):
            error = list_weather_data
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(WeatherSerializer(list_weather_data, many=True).data, status=status.HTTP_201_CREATED)
            # return Response(WeatherSerializer(list_weather_data).data, status=status.HTTP_201_CREATED)


class UpdateTimeView(generics.CreateAPIView):
    """set new time for weather scraping."""
    serializer_class = UpdateTimeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        new_time = self.serializer_class(data=request.data)
        new_time.is_valid(raise_exception=True)
        set_new_time(new_time.validated_data['new_time'])
        return Response({'time_update': 'New scraping time was set'}, status=status.HTTP_200_OK)
