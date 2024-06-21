from django.contrib import admin
from weather.models import Weather


class WeatherAdmin(admin.ModelAdmin):
    """I made WeatherAdmin look like WeatherView. View 6 recent posts """

    list_display = ('date', 'temperature', 'weather_description')
    queryset = Weather.objects.all().order_by('-id')[:6]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Weather, WeatherAdmin)
