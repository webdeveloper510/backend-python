import pytest
from faker import Faker
from django.urls import reverse
from rest_framework import status
from superadmin.subapps.media_and_groupings import serializers_age_groups as serializers
from superadmin.subapps.media_and_groupings import models as m_models

url = reverse('superadmin:media_and_groupings:agegroups')

fake = Faker()

data = {
    "name" : fake.name(),
    "description": fake.text(),
    "min_age" : 1,
    "max_age" : 3,
    "status" : 'INACTIVE',
    }

def test_getRequestWithoutLogin(api_client, ageGroup):    
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    serializer = serializers.AgeGroupSerializer([ageGroup], many=True)
    assert resp.data == serializer.data

def test_getRequestByUser(api_client, user, ageGroup):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    serializer = serializers.AgeGroupSerializer([ageGroup], many=True)
    assert resp.data == serializer.data


def test_getRequestBysuperAdmin(api_client, superAdmin, ageGroup):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    serializer = serializers.AgeGroupSerializer([ageGroup], many=True)
    assert resp.data == serializer.data


def test_getRequestByvendorUser(api_client, vendorUser, ageGroup):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    serializer = serializers.AgeGroupSerializer([ageGroup], many=True)
    assert resp.data == serializer.data


def test_getRequestBysubAdmin(api_client, subAdmin, ageGroup):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    serializer = serializers.AgeGroupSerializer([ageGroup], many=True)
    assert resp.data == serializer.data


def test_postRequestWithoutLogedIn(api_client, country):
    data['country'] = country.name
    # 'name', 'description', 'min_age','max_age', 'country', 'status'
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED

    all_age_groups = m_models.AgeGroup.objects.all()
    assert len(all_age_groups) == 1
    serializer = serializers.AgeGroupSerializer(all_age_groups[0])
    assert resp.data == serializer.data


    #WHEN WE DON'T SEND MAX_AGE
    del data['max_age']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['max_age'] = 3
    
    #WHEN WE DON'T SEND MIN_AGE
    del data['min_age']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    data['min_age']=1

    #  WHEN WE DON'T SEND COUNTRY NEED BAD REQUEST RESPONSE
    del data['country']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


def test_postRequestByUser(api_client, user, country):
    data['country'] = country.name
    # 'name', 'description', 'min_age','max_age', 'country', 'status'
    api_client.force_authenticate(user)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED

    all_age_groups = m_models.AgeGroup.objects.all()
    assert len(all_age_groups) == 1
    serializer = serializers.AgeGroupSerializer(all_age_groups[0])
    assert resp.data == serializer.data


    #WHEN WE DON'T SEND MAX_AGE
    del data['max_age']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['max_age'] = 3
    
    #WHEN WE DON'T SEND MIN_AGE
    del data['min_age']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    data['min_age']=1

    #  WHEN WE DON'T SEND COUNTRY NEED BAD REQUEST RESPONSE
    del data['country']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


def test_postRequestByVendorUser(api_client, vendorUser, country):
    data['country'] = country.name
    # 'name', 'description', 'min_age','max_age', 'country', 'status'
    api_client.force_authenticate(vendorUser)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED

    all_age_groups = m_models.AgeGroup.objects.all()
    assert len(all_age_groups) == 1
    serializer = serializers.AgeGroupSerializer(all_age_groups[0])
    assert resp.data == serializer.data


    #WHEN WE DON'T SEND MAX_AGE
    del data['max_age']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['max_age'] = 3
    
    #WHEN WE DON'T SEND MIN_AGE
    del data['min_age']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    data['min_age']=1

    #  WHEN WE DON'T SEND COUNTRY NEED BAD REQUEST RESPONSE
    del data['country']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

def test_postRequestBySubAdmin(api_client, subAdmin, country):
    data['country'] = country.name
    # 'name', 'description', 'min_age','max_age', 'country', 'status'
    api_client.force_authenticate(subAdmin)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED

    all_age_groups = m_models.AgeGroup.objects.all()
    assert len(all_age_groups) == 1
    serializer = serializers.AgeGroupSerializer(all_age_groups[0])
    assert resp.data == serializer.data


    #WHEN WE DON'T SEND MAX_AGE
    del data['max_age']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['max_age'] = 3
    
    #WHEN WE DON'T SEND MIN_AGE
    del data['min_age']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    data['min_age']=1

    #  WHEN WE DON'T SEND COUNTRY NEED BAD REQUEST RESPONSE
    del data['country']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST






def test_postRequestBySuperAdmin(api_client, superAdmin, country):
    data['country'] = country.name
    # 'name', 'description', 'min_age','max_age', 'country', 'status'
    api_client.force_authenticate(superAdmin)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED

    all_age_groups = m_models.AgeGroup.objects.all()
    assert len(all_age_groups) == 1
    serializer = serializers.AgeGroupSerializer(all_age_groups[0])
    assert resp.data == serializer.data

    

    #WHEN WE DON'T SEND MAX_AGE
    del data['max_age']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data['max_age'] = 3
    
    #WHEN WE DON'T SEND MIN_AGE
    del data['min_age']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    data['min_age']=1

    #  WHEN WE DON'T SEND COUNTRY NEED BAD REQUEST RESPONSE
    del data['country']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST




def test_patchRequestWithoutLogedIn(api_client):
    data = {}
    resp = api_client.patch(url, data=data, format='json')

    assert resp.status_code == 405


def test_patchRequestByUser(api_client, user):
    data = {}
    api_client.force_authenticate(user)
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patchRequestByVendorUser(api_client, vendorUser):
    data = {}
    api_client.force_authenticate(vendorUser)
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patchRequestBysubAdmin(api_client, subAdmin):
    data = {}
    api_client.force_authenticate(subAdmin)
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patchRequestBySuperAdmin(api_client, superAdmin):
    data = {}
    api_client.force_authenticate(superAdmin)
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_putRequestWithoutLogedIn(api_client):
    data = {}
    resp = api_client.put(url, data=data, format='json')

    assert resp.status_code == 405


def test_putRequestByUser(api_client, user):
    data = {}
    api_client.force_authenticate(user)
    resp = api_client.put(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_putRequestByVendorUser(api_client, vendorUser):
    data = {}
    api_client.force_authenticate(vendorUser)
    resp = api_client.put(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_putRequestBysubAdmin(api_client, subAdmin):
    data = {}
    api_client.force_authenticate(subAdmin)
    resp = api_client.put(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_putRequestBySuperAdmin(api_client, superAdmin):
    data = {}
    api_client.force_authenticate(superAdmin)
    resp = api_client.put(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_deleteRequestWithoutLogedIn(api_client):
    data = {}
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == 405


def test_deleteRequestByUser(api_client, user):
    data = {}
    api_client.force_authenticate(user)
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_deleteRequestByVendorUser(api_client, vendorUser):
    data = {}
    api_client.force_authenticate(vendorUser)
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_deleteRequestBysubAdmin(api_client, subAdmin):
    data = {}
    api_client.force_authenticate(subAdmin)
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_deleteRequestBySuperAdmin(api_client, superAdmin):
    data = {}
    api_client.force_authenticate(superAdmin)
    resp = api_client.delete(url, data=data, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED