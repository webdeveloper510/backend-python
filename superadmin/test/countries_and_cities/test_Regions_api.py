import pytest
# from django.conf.urls import url
# from django.db.models.aggregates import Count
from rest_framework import status
# from rest_framework.test import APITestCase
from django.urls.base import reverse
# from django.contrib.auth.models import User
# from rest_framework.test import force_authenticate

from superadmin.subapps.countries_and_cities.models import Country, City, Region, Area, STATUS
from superadmin.subapps.vendor_and_user_management.models import Vendor


# class RegionTestCases(APITestCase):
url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':1})



#     # GET REQUEST TEST CASES
def test_getRequestByNonLoginUser(api_client, country, city):
    resp = api_client.get(url)
    assert resp.status_code == 200

def test_getRequestByUser(api_client, user, country, city):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    
def test_getRequestByVendor(api_client, vendorUser, country, city):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

def test_getRequestBySubAdmin(api_client, subAdmin, country, city):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

def test_getRequestByAdmin(api_client, superAdmin, country, city):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

def test_getRequestByUser(api_client, user, country, city):
    api_client.force_authenticate(user)
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_getRequestVendor(api_client, vendorUser, country, city):
    api_client.force_authenticate(vendorUser)
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_getRequestSubAdmin(api_client, subAdmin, country, city):
    api_client.force_authenticate(subAdmin)
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_getRequestAdmin(api_client, superAdmin, country, city):
    api_client.force_authenticate(superAdmin)
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND


#     # POST REQUEST TEST CASES
@pytest.mark.django_db
def test_postRequestWithoutLogin(api_client):
    resp = api_client.post(url)
    assert resp.status_code == 404

def test_postRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.post(url)
    assert resp.status_code == 404
        

def test_postRequestByVendor(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.post(url)
    assert resp.status_code == 404

def test_postRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    resp = api_client.post(url)
    assert resp.status_code == 404

def test_postRequestBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.post(url)
    assert resp.status_code == 404

# PUT REQUEST TEST CASES
def test_putRequestWithoutLogin(api_client):
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    
def test_putRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_putRequestByVendor(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

# PATCH REQUEST TEST CASES
def test_patchRequestWithOutLogin(api_client):
    resp = api_client.patch(url)
    assert resp.status_code == 405

    
def test_patchRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.patch(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_patchRequestByVendor(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.patch(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_patchRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    resp = api_client.patch(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_patchRequestBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.patch(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

# DELETE REQUEST TEST CASES
@pytest.mark.django_db
def test_deleteRequestWithoutLogin(api_client, country, city):
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    # trying country id is wrong need to get 404 status
    url1 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':1})
    resp = api_client.delete(url1)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
        
    # trying city id is wrong need to get 404 status
    url2 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':10})
    resp = api_client.delete(url2)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    # trying city and country id is wrong need to get 404 status
    url3 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':10})
    resp = api_client.delete(url3)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data = {
        'id_list': ''
    }
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list']= '1234'
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list'] = []
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    region = Region.objects.create(
        name="ASDF",
        status="ACTIVE",
        city=city
    )
    data['id_list'] = [2,5,6]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [2,5,6]
    assert resp.data['success_list'] == []

    data['id_list'] = [region.id, 3]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list']==[3]
    assert resp.data['success_list'] == [region.id]

def test_deleteRequestByUser(api_client, user, country, city):
    api_client.force_authenticate(user)
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    # trying country id is wrong need to get 404 status
    url1 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':1})
    resp = api_client.delete(url1)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
        
    # trying city id is wrong need to get 404 status
    url2 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':10})
    resp = api_client.delete(url2)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    # trying city and country id is wrong need to get 404 status
    url3 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':10})
    resp = api_client.delete(url3)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data = {
        'id_list': ''
    }
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list']= '1234'
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list'] = []
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    region = Region.objects.create(
        name="ASDF",
        status="ACTIVE",
        city=city
    )
    data['id_list'] = [2,5,6]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [2,5,6]
    assert resp.data['success_list'] == []

    data['id_list'] = [region.id, 3]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list']==[3]
    assert resp.data['success_list'] == [region.id]

def test_deleteRequestByVendor(api_client, vendorUser, country, city):
    api_client.force_authenticate(vendorUser)
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    # trying country id is wrong need to get 404 status
    url1 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':1})
    resp = api_client.delete(url1)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
        
    # trying city id is wrong need to get 404 status
    url2 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':10})
    resp = api_client.delete(url2)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    # trying city and country id is wrong need to get 404 status
    url3 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':10})
    resp = api_client.delete(url3)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data = {
        'id_list': ''
    }
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list']= '1234'
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list'] = []
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    region = Region.objects.create(
        name="ASDF",
        status="ACTIVE",
        city=city
    )
    data['id_list'] = [2,5,6]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [2,5,6]
    assert resp.data['success_list'] == []

    data['id_list'] = [region.id, 3]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list']==[3]
    assert resp.data['success_list'] == [region.id]

def test_deleteRequestBySubAdmin(api_client, subAdmin, country, city):
    api_client.force_authenticate(subAdmin)
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    # trying country id is wrong need to get 404 status
    url1 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':1})
    resp = api_client.delete(url1)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
        
    # trying city id is wrong need to get 404 status
    url2 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':10})
    resp = api_client.delete(url2)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    # trying city and country id is wrong need to get 404 status
    url3 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':10})
    resp = api_client.delete(url3)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data = {
        'id_list': ''
    }
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list']= '1234'
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list'] = []
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    region = Region.objects.create(
        name="ASDF",
        status="ACTIVE",
        city=city
    )
    data['id_list'] = [2,5,6]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [2,5,6]
    assert resp.data['success_list'] == []

    data['id_list'] = [region.id, 3]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list']==[3]
    assert resp.data['success_list'] == [region.id]
    
def test_deleteRequestByAdmin(api_client, superAdmin, country, city):
    api_client.force_authenticate(superAdmin)
    url = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    # trying country id is wrong need to get 404 status
    url1 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':1})
    resp = api_client.delete(url1)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
        
    # trying city id is wrong need to get 404 status
    url2 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':1, 'city':10})
    resp = api_client.delete(url2)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    # trying city and country id is wrong need to get 404 status
    url3 = reverse('superadmin:countries_and_cities:Regions', kwargs={'country':10, 'city':10})
    resp = api_client.delete(url3)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data = {
        'id_list': ''
    }
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list']= '1234'
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list'] = []
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    region = Region.objects.create(
        name="ASDF",
        status="ACTIVE",
        city=city
    )
    data['id_list'] = [2,5,6]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [2,5,6]
    assert resp.data['success_list'] == []

    data['id_list'] = [region.id, 3]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list']==[3]
    assert resp.data['success_list'] == [region.id]