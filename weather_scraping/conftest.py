import pytest
from rest_framework.test import APIClient


"""created custom users"""
@pytest.fixture
def api_client():
    return APIClient()
