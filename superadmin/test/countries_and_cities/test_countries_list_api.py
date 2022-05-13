import pytest
# from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
# from rest_framework.test import APITestCase
from rest_framework import status
from superadmin.subapps.countries_and_cities import serializers

from superadmin.subapps.countries_and_cities.models import Country, City, Region, Area
from superadmin.subapps.countries_and_cities.serializers import CountrySerializer
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator

url = reverse('superadmin:countries_and_cities:unsecured_countries')

@pytest.mark.django_db
def test_get_api_data(api_client):
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountrySerializer(countries, many=True)
    assert serializer.data == resp.data

@pytest.mark.django_db
def test_get_data_with_params(api_client):
    # url = reverse('superadmin:countries_and_cities:unsecured_countries', kwargs={'perpage': '1'})
    url = "%s?perpage=1" % reverse('superadmin:countries_and_cities:unsecured_countries')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountrySerializer(countries, many=True)
    assert resp.data['results'] == serializer.data



def test_post_api_not_allowed(api_client):
    data= {
        "name": "CANADA"
    }
    resp = api_client.post(url, data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_put_api_not_allowed(api_client):
    data= {
        "name": "CANADA"
    }
    resp = api_client.put(url, data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_post_api_not_allowed(api_client):
    data= {
        "name": "CANADA"
    }
    resp = api_client.patch(url, data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_post_api_not_allowed(api_client):
    data= {
        "name": "CANADA"
    }
    resp = api_client.delete(url, data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
