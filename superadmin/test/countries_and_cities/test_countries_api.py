import pytest
from django.urls import reverse
from rest_framework import status
from superadmin.subapps.countries_and_cities.models import Country, City, Area, Region
from superadmin.subapps.countries_and_cities.serializers import CountrySerializer, CountryCompactSerializer
from superadmin.subapps.vendor_and_user_management.models import Vendor


# class countriesTest(APITestCase):
url = reverse('superadmin:countries_and_cities:countries')
    
data = {
        "name": "Affrica1",
        "abbr": "AF",
        "cities": [
            {
                "id": 1,
                "name": "Kolkata",
                "regions": [
                    {
                        "id": 1,
                        "name": "Rm1",
                        "status": "ACTIVE",
                        "no_of_areas": 2,
                        "areas": [
                            {
                                "id": 1,
                                "name": "A1a",
                                "status": "ACTIVE"
                            },
                            {
                                "id": 7,
                                "name": "A2a",
                                "status": "ACTIVE"
                            }
                        ]
                    },
                    {
                        "id": 17,
                        "name": "Rm2",
                        "status": "ACTIVE",
                        "no_of_areas": 2,
                        "areas": [
                            {
                                "id": 1,
                                "name": "A1a",
                                "status": "ACTIVE"
                            },
                            {
                                "id": 7,
                                "name": "A2a",
                                "status": "ACTIVE"
                            }
                        ]
                    }
                ]
            }
        ],
        "currency": {
            "display_character": "$",
            "name": "Dollar"
        }
    }
    

def test_getRequestWithoutSignin(api_client, country, city):
    url = reverse('superadmin:countries_and_cities:countries')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountrySerializer(countries, many=True)
    assert resp.data == serializer.data

    # request with ""mode = compact"" query parameter
    url1 = url + '?mode=compact'
    resp = api_client.get(url1)
    assert resp.status_code == status.HTTP_200_OK
    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountryCompactSerializer(countries, many=True)
    assert resp.data == serializer.data

        # request with "perpage=1" query paramas
    url2 = url + '?perpage=1'
    resp = api_client.get(url2)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data['results']) == 1
        
        
    # request with "?perpage=1&mode=compact" query paramas
    url3 = url + '?perpage=1&mode=compact'
    resp = api_client.get(url3)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data['results']) == 1

    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountryCompactSerializer(countries, many=True)
    assert resp.data['results'] == serializer.data

def test_getRequestByUser(api_client, user, country, city):
    api_client.force_authenticate(user)
    url = reverse('superadmin:countries_and_cities:countries')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountrySerializer(countries, many=True)
    assert resp.data == serializer.data

    # request with ""mode = compact"" query parameter
    url1 = url + '?mode=compact'
    resp = api_client.get(url1)
    assert resp.status_code == status.HTTP_200_OK
    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountryCompactSerializer(countries, many=True)
    assert resp.data == serializer.data

        # request with "perpage=1" query paramas
    url2 = url + '?perpage=1'
    resp = api_client.get(url2)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data['results']) == 1
        
        
    # request with "?perpage=1&mode=compact" query paramas
    url3 = url + '?perpage=1&mode=compact'
    resp = api_client.get(url3)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data['results']) == 1

    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountryCompactSerializer(countries, many=True)
    assert resp.data['results'] == serializer.data
    
def test_getRequestBySuperUser(api_client, superAdmin, country):
    api_client.force_authenticate(superAdmin)
    url = reverse('superadmin:countries_and_cities:countries')
    # request without any query params
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountrySerializer(countries, many=True)
    assert resp.data == serializer.data

    # request with ""mode = compact"" query parameter
    url1 = url + '?mode=compact'
    resp = api_client.get(url1)
    assert resp.status_code == status.HTTP_200_OK
    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountryCompactSerializer(countries, many=True)
    assert resp.data == serializer.data

    # request with "perpage=1" query paramas
    url2 = url + '?perpage=1'
    resp = api_client.get(url2)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data['results']) == 1
        
        
    # request with "?perpage=1&mode=compact" query paramas
    url3 = url + '?perpage=1&mode=compact'
    resp = api_client.get(url3)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data['results']) == 1

    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountryCompactSerializer(countries, many=True)
    assert resp.data['results'] == serializer.data
    
def test_getRequestByVendor(api_client, vendorUser, country):
    api_client.force_authenticate(vendorUser)
    # request without any query params
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountrySerializer(countries, many=True)
    assert resp.data == serializer.data

    # request with ""mode = compact"" query parameter
    url1 = url + '?mode=compact'
    resp = api_client.get(url1)
    assert resp.status_code == status.HTTP_200_OK
    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountryCompactSerializer(countries, many=True)
    assert resp.data == serializer.data

    # request with "perpage=1" query paramas
    url2 = url + '?perpage=1'
    resp = api_client.get(url2)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data['results']) == 1
        
        
    # request with "?perpage=1&mode=compact" query paramas
    url2 = url + '?perpage=1&mode=compact'
    resp = api_client.get(url2)
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data['results'])==1

    countries = Country.objects.filter(status="ACTIVE")
    serializer = CountryCompactSerializer(countries, many=True)
    assert resp.data['results'] == serializer.data

@pytest.mark.django_db
def test_postRequestWithoutLogin(api_client):
    data['cities'][0]['regions'][0]['areas'][0]['name'] = 'B' 
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['cities'][0]['regions'][0]['areas'][0]['name'] = 'A1a' 

def test_postRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    data['cities'][0]['name'] = 'B' 
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['cities'][0]['name'] = 'Kolkata' 

def test_postRequestBySuperUser(api_client, superAdmin):
    api_client.force_authenticate(user=superAdmin)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED

def test_postRequestByVendor(api_client,user):
    api_client.force_authenticate(user)
    data['name'] = 'A'
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['name'] = 'Africa'
    
    
    
def test_postRequestLessthanThreeCharecterNameBySuperAdmin(api_client, superAdmin):

    # 1. country name must be three charecter
    data['name'] = 'A'
    api_client.force_authenticate(user=superAdmin)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['name'] = 'Africa'

def test_postRequestLessThanThreeCharecterOfCityNameBySuperAdmin(api_client, superAdmin):
    # 2. city name must be three charecter
    data['cities'][0]['name'] = 'B' 
    api_client.force_authenticate(user=superAdmin)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['cities'][0]['name'] = 'Kolkata' 

def test_postRequestLessThanThreeCharecterOfRegionBySuperAdmin(api_client, superAdmin):
    # 3. region name must be three charecter
    data['cities'][0]['regions'][0]['name'] = 'B' 
    api_client.force_authenticate(superAdmin)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['cities'][0]['regions'][0]['name'] = 'Rm1' 
    
def test_postRequestLessThanThreeCharecterOfRegionBySuperAdmini(api_client, superAdmin):
    # 4. area name must be three charecter
    data['cities'][0]['regions'][0]['areas'][0]['name'] = 'B' 
    api_client.force_authenticate(superAdmin)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['cities'][0]['regions'][0]['areas'][0]['name'] = 'A1a' 
    

def test_putRequestByUser(api_client, user):
    data = {
        "name": "Kolkata"
    }
    api_client.force_authenticate(user)
    resp = api_client.put(url, data=data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_putRequestBySuperUser(api_client, superAdmin):
    data = {
        "name": "Kolkata"
    }
    api_client.force_authenticate(superAdmin)
    resp = api_client.put(url, data=data)
    assert resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestByVendor(api_client, vendorUser):
    data = {
        "name": "Kolkata"
    }
    api_client.force_authenticate(vendorUser)
    resp = api_client.put(url, data=data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_patchRequestByUser(api_client, user):
    data = {
        "name": "Kolkata"
    }
    api_client.force_authenticate(user)
    resp = api_client.patch(url, data=data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_putRequestBySuperUser(api_client, superAdmin):
    data = {
        "name": "Kolkata"
    }
    api_client.force_authenticate(superAdmin)
    resp = api_client.patch(url, data=data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_putRequestByVendor(api_client, vendorUser):
    data = {
        "name": "Kolkata"
    }
    api_client.force_authenticate(vendorUser)
    resp = api_client.patch(url, data=data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_deleteRequestByUser(api_client, user):
    data = {
        "name": "Kolkata"
    }
    api_client.force_authenticate(user)
    resp = api_client.delete(url, data=data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_deleteRequestBySuperUser(api_client, superAdmin):
    data = {
        "name": "Kolkata"
    }
    api_client.force_authenticate(superAdmin)
    resp = api_client.delete(url, data=data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_deleteRequestByVendor(api_client, vendorUser):
    data = {
        "name": "Kolkata"
    }
    api_client.force_authenticate(vendorUser)
    resp = api_client.delete(url, data=data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    

