import pytest
import datetime
from django.urls import reverse
from django.utils import timezone


class TestView:
    @pytest.mark.django_db
    def test_list_weather_valid(self, api_client):
        response = api_client.get(reverse('update_weather'), format='json')
        assert response.status_code == 201
        response_1 = api_client.get(reverse('list_weather'), format='json')
        assert response_1.status_code == 200
        response_json = response_1.json()
        assert response_json
        assert response_json['count'] == 6

    @pytest.mark.django_db
    def test_update_weather_valid(self, api_client):
        response = api_client.get(reverse('update_weather'), format='json')
        assert response.status_code == 201
        response_json = response.json()
        assert response_json
        assert len(response_json) == 6

    def test_time_update_valid(self, api_client):
        response = api_client.post(reverse('time_update'), {'new_time': timezone.now() + datetime.timedelta(hours=1)},
                                   format='json')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json
        assert response_json['time_update'] == 'New scraping time was set'
