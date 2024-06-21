import time
from requests import get
from bs4 import BeautifulSoup

from celery_app.celery import app
from weather.models import Weather
from celery.schedules import crontab


class WeatherScraping:
    """This class makes a basic request to https://ua.sinoptik.ua/ and then parses the result """
    __slots__ = ('accept', 'maine_url', 'retry_count', 'response', 'data_to_save', 'days_number')

    def __init__(self):
        self.accept = 200
        self.maine_url = 'https://ua.sinoptik.ua/'
        self.retry_count = 5
        self.days_number = 6
        self.response = self.make_request(self.maine_url)
        self.data_to_save = []

    def make_request(self, url):
        """Makes a request; in case of a negative result, repeats the request 5 times """
        response = get(url)
        if response.status_code == self.accept:
            return response.content
        else:
            if self.retry_count > 0:
                time.sleep(2)
                self.retry_count -= 1
                return self.make_request(url)
            else:
                return False

    def perform_scraping(self):
        """The process of parsing the response. Data preparation. Writing data to the list """
        raw_data = BeautifulSoup(self.response, 'html.parser')
        weather_blocks = raw_data.find_all('div', class_='main')
        for weather in weather_blocks:
            if self.days_number > 0:
                if not (date := weather.find('a', class_='day-link')):
                    date = weather.find('p', class_='day-link')
                data_to_save = {
                    'date': date['data-link'].split('/')[-1],
                    'temperature': int(weather.find('div', class_='min').span.text.replace('°', '').strip()),
                    'weather_description': weather.find('div', class_='weatherIco')['title'],
                }
                self.data_to_save.append(Weather(**data_to_save))
                self.days_number -= 1


def perform_weather_scraping():
    weather = WeatherScraping()
    if response := weather.response:
        weather.perform_scraping()
        try:
            """bulk will write all the data to the database. If there are existing records, it will update them. """
            Weather.objects.bulk_create(weather.data_to_save, batch_size=6, update_conflicts=True,
                                        update_fields=['temperature', 'weather_description'], unique_fields=['date'])
            return weather.data_to_save
        except Exception as e:
            return {'error': 'There is a problem. Contact the site administrator'}
    else:
        return {'error': 'The requested resource is not responding. Please try again later'}


def set_new_time(new_time):
    """Mechanism for updating the task execution time """
    new_hour = new_time.hour
    new_minute = new_time.minute
    app.conf.beat_schedule['perform_weather_scraping_task']['schedule'] = crontab(hour=new_hour,
                                                                                  minute=new_minute)
    app.conf.update(CELERY_BEAT_SCHEDULE=app.conf.beat_schedule)
