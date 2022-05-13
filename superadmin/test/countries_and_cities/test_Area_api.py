import pytest
from rest_framework import status
from django.urls.base import reverse

from superadmin.subapps.countries_and_cities.models import Country, City, Region, Area, STATUS
from superadmin.subapps.vendor_and_user_management.models import Vendor


url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1, 'region':1})

    
#     # GET REQUEST TEST CASES
def test_getRequestByNonLoginUser(api_client, country, city, region, area):
    resp = api_client.get(url)
    assert resp.status_code == 200

def test_getRequestByUser(api_client, user, country, city, region, area):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

def test_getRequestByVendor(api_client, vendorUser, country, city, region, area):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

def test_getRequestBySubAdmin(api_client, subAdmin, country, city, region, area):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

def test_getRequestByAdmin(api_client, superAdmin, country, city, region, area):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

def test_getRequestByUser(api_client, user, country, city, region, area):
    api_client.force_authenticate(user)
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':1, 'region':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
        
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':10, 'region':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1, 'region':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':10, 'region':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_getRequestVendor(api_client, vendorUser, country, city, region, area):
    api_client.force_authenticate(vendorUser)
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':1, 'region':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':10, 'region':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1, 'region':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':10, 'region':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_getRequestSubAdmin(api_client, subAdmin, country, city, region, area):
    api_client.force_authenticate(subAdmin)
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':1, 'region':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':10, 'region':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1, 'region':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':10, 'region':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_getRequestAdmin(api_client, superAdmin, country, city, region, area):
    api_client.force_authenticate(superAdmin)
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':1, 'region':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':10, 'region':1})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1, 'region':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':10, 'region':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND


# # POST REQUEST TEST CASES
def test_postRequestWithoutLogin(api_client):
    resp = api_client.post(url)
    assert resp.status_code == 405

def test_postRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        

def test_postRequestByVendor(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_postRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_postRequestBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

#     # PUT REQUEST TEST CASES
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

#     # PATCH REQUEST TEST CASES
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

def test_patchRequestBySuperAdmin(api_client,superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.patch(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

#     # DELETE REQUEST TEST CASES
def test_deleteRequestWithoutLogin(api_client, country, city, region, area):
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1, 'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
def test_deleteRequestByUser(api_client, user,  country, city, region, area):
    api_client.force_authenticate(user)
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1, 'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
        
    # trying country id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':1, 'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
        
    # trying city id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':10,  'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    # trying city and country id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1,  'region':10})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data = {
        'id_list': ''
    }
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1,  'region':1})
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list']= '1234'
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    data['id_list'] = []
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    area = Area.objects.create(
        name="ASDF",
        status="ACTIVE",
        region=region
    )

    data['id_list'] = [3,5,6]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [3,5,6]
    assert resp.data['success_list'] == []

    data['id_list'] = [area.id, 3]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [3]
    assert resp.data['success_list'] == [area.id]
    
def test_deleteRequestByVendor(api_client, vendorUser,  country, city, region, area):
    api_client.force_authenticate(vendorUser)
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1, 'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
        
    # trying country id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':1, 'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
        
    # trying city id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':10,  'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    # trying city and country id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1,  'region':10})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data = {
        'id_list': ''
    }
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1,  'region':1})
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list']= '1234'
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    data['id_list'] = []
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    area = Area.objects.create(
        name="ASDF",
        status="ACTIVE",
        region=region
    )

    data['id_list'] = [3,5,6]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [3,5,6]
    assert resp.data['success_list'] == []

    data['id_list'] = [area.id, 3]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [3]
    assert resp.data['success_list'] == [area.id]

def test_deleteRequestBySubAdmin(api_client, subAdmin, country, city, region, area):
    api_client.force_authenticate(subAdmin)
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1, 'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
        
    # trying country id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':1, 'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
        
    # trying city id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':10,  'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    # trying city and country id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1,  'region':10})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data = {
        'id_list': ''
    }
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1,  'region':1})
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list']= '1234'
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    data['id_list'] = []
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    area = Area.objects.create(
        name="ASDF",
        status="ACTIVE",
        region=region
    )

    data['id_list'] = [3,5,6]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [3,5,6]
    assert resp.data['success_list'] == []

    data['id_list'] = [area.id, 3]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [3]
    assert resp.data['success_list'] == [area.id]

def test_deleteRequestByAdmin(api_client, superAdmin, country, city, region, area):
    api_client.force_authenticate(superAdmin)
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1, 'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
        
    # trying country id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':10, 'city':1, 'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
        
    # trying city id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':10,  'region':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
    # trying city and country id is wrong need to get 404 status
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1,  'region':10})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    data = {
        'id_list': ''
    }
    url = reverse('superadmin:countries_and_cities:Area', kwargs={'country':1, 'city':1,  'region':1})
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    
    data['id_list']= '1234'
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    data['id_list'] = []
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    area = Area.objects.create(
        name="ASDF",
        status="ACTIVE",
        region=region
    )

    data['id_list'] = [3,5,6]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [3,5,6]
    assert resp.data['success_list'] == []

    data['id_list'] = [area.id, 3]
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert resp.data['failed_list'] == [3]
    assert resp.data['success_list'] == [area.id]
