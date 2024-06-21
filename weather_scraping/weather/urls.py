from django.urls import path
from weather.views import WeatherView, UpdaterWeatherView, UpdateTimeView

urlpatterns = [
    path('weather/', WeatherView.as_view(), name='list_weather'),
    path('weather/update', UpdaterWeatherView.as_view(), name='update_weather'),
    path('weather/time_update', UpdateTimeView.as_view(), name='time_update'),
]
