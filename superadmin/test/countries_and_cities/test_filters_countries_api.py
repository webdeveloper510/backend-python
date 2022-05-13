import pytest
# from django.conf.urls import url
# from django.db.models import manager
from django.urls import reverse
from rest_framework import status
from superadmin.subapps.countries_and_cities.models import Country
from superadmin.subapps.countries_and_cities.serializers import CountryListFilterSerializer

url = reverse('superadmin:countries_and_cities:countrieslist')

@pytest.mark.django_db
def test_getRequest(api_client):
    resp = api_client.get(url)    
    assert resp.status_code == status.HTTP_200_OK
    countries = Country.objects.filter(status='ACTIVE')
    serializer = CountryListFilterSerializer(countries, many=True)
    assert resp.data == serializer.data


@pytest.mark.django_db
def test_paginationRequest(api_client):
    url = reverse('superadmin:countries_and_cities:countrieslist')

    Country.objects.create(
        name="Indonesia",
        abbr="Indo",
        status="ACTIVE"
    )
    Country.objects.create(
        name="Nepal",
        abbr="Nepal",
        status="ACTIVE"
    )
    Country.objects.create(
        name="Bhutan",
        abbr="Bhutan",
        status="ACTIVE"
    )
    url = "%s?perpage=1"%(url)
    resp = api_client.get(url) 
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data['results'])== 1

def test_post_request_not_allowed(api_client):
    resp = api_client.post(url)   
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
def test_put_request_not_allowed(api_client):
    resp = api_client.put(url)   
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_patch_request_not_allowed(api_client):
    resp = api_client.patch(url)   
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_delete_request_not_allowed(api_client):
    resp = api_client.delete(url)   
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
