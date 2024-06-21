from celery import shared_task
from weather.business_logic import perform_weather_scraping


@shared_task
def perform_weather_scraping_task():
    perform_weather_scraping()
