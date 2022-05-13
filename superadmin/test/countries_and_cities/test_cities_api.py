import pytest
from superadmin.subapps.countries_and_cities.views import Cities
from django.urls.base import reverse
from rest_framework import status
from superadmin.subapps.countries_and_cities.models import Country, City, Area, Region
from superadmin.subapps.countries_and_cities.serializers import CitySerializer
from superadmin.subapps.vendor_and_user_management.models import Vendor

url = reverse("superadmin:countries_and_cities:cities", kwargs={'cid':1})
addCountryDataUrl = reverse('superadmin:countries_and_cities:countries')

def test_getRequestWithoutLogin(api_client,country):
    resp = api_client.get(url)
    assert resp.status_code == 200
    city_obj = City.objects.filter(country__id=1, status='ACTIVE')
    serializer = CitySerializer(city_obj, many=True)
    assert resp.data == serializer.data

def test_getCityDetailsByUser(api_client, user, country):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    city_obj = City.objects.filter(country__id=1, status='ACTIVE')
    serializer = CitySerializer(city_obj, many=True)
    assert resp.data == serializer.data
    
def test_getCityDetailsBySubAdmin(api_client, subAdmin, country):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    city_obj = City.objects.filter(country__id=1, status='ACTIVE')
    serializer = CitySerializer(city_obj, many=True)
    assert resp.data == serializer.data
    
def test_getCityDetailsBySuperAdmin(api_client, superAdmin, country):
    # self.postRequestBySuperUser()
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    city_obj = City.objects.filter(country__id=1, status='ACTIVE')
    serializer = CitySerializer(city_obj, many=True)
    assert resp.data == serializer.data

def test_getCityDetailsByVendor(api_client, vendorUser, country):
    # self.postRequestBySuperUser()
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    city_obj = City.objects.filter(country__id=1, status='ACTIVE')
    serializer = CitySerializer(city_obj, many=True)
    assert resp.data == serializer.data

def test_putRequestWithoutLogin(api_client, country):
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    
def test_putRequestByUser(api_client,user, country):
    # self.postRequestBySuperUser()
    api_client.force_authenticate(user)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_putRequestBySubAdmin(api_client,subAdmin, country):
    # self.postRequestBySuperUser()
    api_client.force_authenticate(subAdmin)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_putRequestBySuperAdmin(api_client,subAdmin, country):
    # self.postRequestBySuperUser()
    api_client.force_authenticate(subAdmin)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_putRequestByVendor(api_client,vendorUser, country):
    # self.postRequestBySuperUser()
    api_client.force_authenticate(vendorUser)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_patchRequestWithoutLogin(api_client):
    resp = api_client.patch(url)
    assert resp.status_code == 405

def test_patchRequestByUser(api_client, user, country):
    # self.postRequestBySuperUser()
    api_client.force_authenticate(user)
    resp = api_client.patch(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_patchRequestBySubAdmin(api_client, subAdmin, country):
    # self.postRequestBySuperUser()
    api_client.force_authenticate(subAdmin)
    resp = api_client.patch(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_patchRequestBySuperAdmin(api_client, superAdmin, country):
    # self.postRequestBySuperUser()
    api_client.force_authenticate(superAdmin)
    resp = api_client.patch(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_patchRequestByVendor(api_client, vendorUser, country):
    # self.postRequestBySuperUser()
    api_client.force_authenticate(vendorUser)
    resp = api_client.patch(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    

@pytest.mark.django_db
def test_postRequestWithoutLogin(api_client):
    data={
        'name'
    }
    Country.objects.create(
        name="INDIA",
        status="ACTIVE",
        abbr='IN'
    )
    data = {
        'status': "ACTIVE",
        'name': "Kolkata"
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
        
    data = {
        'status': "ACTIVE",
        'name': "Ko"
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    
    data = {
        'status': "ACTIVE",
        'name': "Pune",
        'regions': {
            'name': "Kharadi"
        }
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data = {
        'status': "ACTIVE",
        'name': "Pune",
        'regions': [{
            'name': "Kharadi",
            'status': "ACTIVE"
        }]
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
    # City.objects.get(name='Pune')
    regions = Region.objects.filter(city__name='Pune').count()
    assert regions == 1
    
    data['regions'][0]['name'] = 'KH'
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    
    data['regions'][0]['name'] = 'Kharadi'
    data['regions'][0]['areas']={'name': "Areas", 'status': 'ACTIVE'}
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


    data['regions'][0]['areas']=[{'name': "Areas", 'status': 'ACTIVE'}]
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
    areasInKharadi = Area.objects.filter(region__name="Kharadi").count()
    assert areasInKharadi == 1

def test_postRequestByUser(api_client, user, country):
    api_client.force_authenticate(user)
    Country.objects.create(
        name="INDIA",
        status="ACTIVE",
        abbr='IN'
    )
    data = {
        'status': "ACTIVE",
        'name': "Kolkata"
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
        
    data = {
        'status': "ACTIVE",
        'name': "Ko"
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    
    data = {
        'status': "ACTIVE",
        'name': "Pune",
        'regions': {
            'name': "Kharadi"
        }
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data = {
        'status': "ACTIVE",
        'name': "Pune",
        'regions': [{
            'name': "Kharadi",
            'status': "ACTIVE"
        }]
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
    # City.objects.get(name='Pune')
    regions = Region.objects.filter(city__name='Pune').count()
    assert regions == 1
    
    data['regions'][0]['name'] = 'KH'
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    
    data['regions'][0]['name'] = 'Kharadi'
    data['regions'][0]['areas']={'name': "Areas", 'status': 'ACTIVE'}
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


    data['regions'][0]['areas']=[{'name': "Areas", 'status': 'ACTIVE'}]
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
    areasInKharadi = Area.objects.filter(region__name="Kharadi").count()
    assert areasInKharadi == 1
    
def test_postRequestByVendor(api_client, vendorUser, country):
    api_client.force_authenticate(vendorUser)
    Country.objects.create(
        name="INDIA",
        status="ACTIVE",
        abbr='IN'
    )
    data = {
        'status': "ACTIVE",
        'name': "Kolkata"
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
        
    data = {
        'status': "ACTIVE",
        'name': "Ko"
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    
    data = {
        'status': "ACTIVE",
        'name': "Pune",
        'regions': {
            'name': "Kharadi"
        }
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data = {
        'status': "ACTIVE",
        'name': "Pune",
        'regions': [{
            'name': "Kharadi",
            'status': "ACTIVE"
        }]
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
    # City.objects.get(name='Pune')
    regions = Region.objects.filter(city__name='Pune').count()
    assert regions == 1
    
    data['regions'][0]['name'] = 'KH'
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    
    data['regions'][0]['name'] = 'Kharadi'
    data['regions'][0]['areas']={'name': "Areas", 'status': 'ACTIVE'}
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


    data['regions'][0]['areas']=[{'name': "Areas", 'status': 'ACTIVE'}]
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
    areasInKharadi = Area.objects.filter(region__name="Kharadi").count()
    assert areasInKharadi == 1

def test_postRequestBySubAdmin(api_client, subAdmin, country):
    api_client.force_authenticate(subAdmin)
    Country.objects.create(
        name="INDIA",
        status="ACTIVE",
        abbr='IN'
    )
    data = {
        'status': "ACTIVE",
        'name': "Kolkata"
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED

        
    data = {
        'status': "ACTIVE",
        'name': "Ko"
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data = {
        'status': "ACTIVE",
        'name': "Pune",
        'regions': {
            'name': "Kharadi"
        }
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data = {
        'status': "ACTIVE",
        'name': "Pune",
        'regions': [{
            'name': "Kharadi",
            'status': "ACTIVE"
        }]
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
    # City.objects.get(name='Pune')
    regions = Region.objects.filter(city__name='Pune').count()
    assert regions, 1
        
    data['regions'][0]['name'] = 'KH'
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    
    data['regions'][0]['name'] = 'Kharadi'
    data['regions'][0]['areas']={'name': "Areas", 'status': 'ACTIVE'}
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


    data['regions'][0]['areas']=[{'name': "Areas", 'status': 'ACTIVE'}]
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code== status.HTTP_201_CREATED
    areasInKharadi = Area.objects.filter(region__name="Kharadi").count()
    assert areasInKharadi == 1
    
def test_postRequestBySuperAdmin(api_client, superAdmin, country):
    api_client.force_authenticate(superAdmin)
    Country.objects.create(
        name="INDIA",
        status="ACTIVE",
        abbr='IN'
    )
    data = {
        'status': "ACTIVE",
        'name': "Kolkata"
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
        
    data = {
        'status': "ACTIVE",
        'name': "Ko"
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    
    data = {
        'status': "ACTIVE",
        'name': "Pune",
        'regions': {
            'name': "Kharadi"
        }
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data = {
        'status': "ACTIVE",
        'name': "Pune",
        'regions': [{
            'name': "Kharadi",
            'status': "ACTIVE"
        }]
    }
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
    # City.objects.get(name='Pune')
    regions = Region.objects.filter(city__name='Pune').count()
    assert regions == 1
    
    data['regions'][0]['name'] = 'KH'
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    
    data['regions'][0]['name'] = 'Kharadi'
    data['regions'][0]['areas']={'name': "Areas", 'status': 'ACTIVE'}
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


    data['regions'][0]['areas']=[{'name': "Areas", 'status': 'ACTIVE'}]
    resp = api_client.post(url, data=data, format='json') 
    assert resp.status_code == status.HTTP_201_CREATED
    areasInKharadi = Area.objects.filter(region__name="Kharadi").count()
    assert areasInKharadi == 1

def test_deleteRequestByNotLoginUser(api_client, country):
    Country.objects.create(
        name="Singapore",
        status="ACTIVE",
        abbr='IN'
    )
    url = reverse("superadmin:countries_and_cities:cities", kwargs={'cid':1})
    
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    url1 = reverse("superadmin:countries_and_cities:cities", kwargs={'cid':10})
    resp = api_client.delete(url1)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data={
        'id_list': [1,2,3]
    }

    resp = api_client.delete(url, data=data,format='json')
    assert resp.data['failed_list'], [1,2,3]
    assert resp.data['success_list'] == []
    
def test_deleteRequestByUser(api_client, user, country):
    api_client.force_authenticate(user)
    Country.objects.create(
        name="Singapore",
        status="ACTIVE",
        abbr='IN'
    )
    url = reverse("superadmin:countries_and_cities:cities", kwargs={'cid':1})
    
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    url1 = reverse("superadmin:countries_and_cities:cities", kwargs={'cid':10})
    resp = api_client.delete(url1)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data={
        'id_list': [1,2,3]
    }

    resp = api_client.delete(url, data=data,format='json')
    assert resp.data['failed_list'], [1,2,3]
    assert resp.data['success_list'] == []
    
def test_deleteRequestByVendor(api_client, vendorUser, country):
    api_client.force_authenticate(vendorUser)
    Country.objects.create(
        name="Singapore",
        status="ACTIVE",
        abbr='IN'
    )
    url = reverse("superadmin:countries_and_cities:cities", kwargs={'cid':1})
    
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    url1 = reverse("superadmin:countries_and_cities:cities", kwargs={'cid':10})
    resp = api_client.delete(url1)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data={
        'id_list': [1,2,3]
    }

    resp = api_client.delete(url, data=data,format='json')
    assert resp.data['failed_list'], [1,2,3]
    assert resp.data['success_list'] == []
    
def test_deleteRequestBySubAdmin(api_client, subAdmin, country):
    
    api_client.force_authenticate(subAdmin)
    Country.objects.create(
        name="Singapore",
        status="ACTIVE",
        abbr='IN'
    )
    url = reverse("superadmin:countries_and_cities:cities", kwargs={'cid':1})
    
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    url1 = reverse("superadmin:countries_and_cities:cities", kwargs={'cid':10})
    resp = api_client.delete(url1)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data={
        'id_list': [1,2,3]
    }

    resp = api_client.delete(url, data=data,format='json')
    assert resp.data['failed_list'], [1,2,3]
    assert resp.data['success_list'] == []

def test_deleteRequestByAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    Country.objects.create(
        name="Singapore",
        status="ACTIVE",
        abbr='IN'
    )
    url = reverse("superadmin:countries_and_cities:cities", kwargs={'cid':1})
    
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    url1 = reverse("superadmin:countries_and_cities:cities", kwargs={'cid':10})
    resp = api_client.delete(url1)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data={
        'id_list': [1,2,3]
    }

    resp = api_client.delete(url, data=data,format='json')
    assert resp.data['failed_list'], [1,2,3]
    assert resp.data['success_list'] == []



