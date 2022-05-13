import pytest
from django.urls import reverse
from rest_framework import status
from superadmin.subapps.countries_and_cities.models import Country, City, Area, Region
from superadmin.subapps.countries_and_cities.serializers import CityListFilterSerializer


url = "%s?country_id=1"% reverse('superadmin:countries_and_cities:citieslist')


def test_getRequest(api_client, city):
    resp = api_client.get(url)
    cities = City.objects.filter(country__id=1, status="ACTIVE")
    serializer = CityListFilterSerializer(cities, many=True)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data == serializer.data

def test_without_countryId(api_client):
    url = reverse('superadmin:countries_and_cities:citieslist')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
def test_getRequestPagination(api_client, country):
    url = "%s?country_id=1"% reverse('superadmin:countries_and_cities:citieslist')

    City.objects.create(
        name = 'Pune',
        country = country,
        status = "ACTIVE",
        # created_by = self.user,
    )
    City.objects.create(
        name = 'Kolkata',
        country = country,
        status = "ACTIVE",
        # created_by = self.user,
    )
    City.objects.create(
        name = 'Hydrabad',
        country = country,
        status = "ACTIVE",
        # created_by = self.user,
    )
    url = url + '&perpage=1'

    resp = api_client.get(url)
    assert len(resp.data['results']) == 1

def test_postRequest(api_client):
    data ={
        'name': 'Bangalore'
    }
    resp = api_client.post(url, data=data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequest(api_client):
    data = {
        'name': "Bangalore" 
    }
    resp = api_client.put(url, data=data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_patchRequest(api_client):
    data ={
        'name': 'Bangalore'
    }
    resp = api_client.patch(url, data=data)
    assert resp.status_code== status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_deleteRequest(api_client):
    data ={
        'name': 'Bangalore'
    }
    resp = api_client.delete(url, data=data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    