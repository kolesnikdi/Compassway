from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Weather(models.Model):
    date = models.DateField(unique=True)
    temperature = models.SmallIntegerField(validators=[MinValueValidator(-99), MaxValueValidator(99)])
    weather_description = models.CharField(max_length=255)
