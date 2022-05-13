import pytest
from faker import Faker
from django.urls import reverse
from rest_framework import status

from superadmin.subapps.media_and_groupings.models import AgeGroup
from superadmin.subapps.media_and_groupings import serializers_age_groups as serializers


url = reverse('superadmin:media_and_groupings:agegroups_filter', kwargs={'id':1})

def test_getRequestWithoutLogin(api_client, ageGroup):
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    filteredAgeGroup = AgeGroup.objects.filter(country__id=ageGroup.id)
    serializer = serializers.AgeGroupSerializer(filteredAgeGroup, many=True)    
    assert resp.data == serializer.data

def test_getRequestByUser(api_client, user, ageGroup):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    filteredAgeGroup = AgeGroup.objects.filter(country__id=ageGroup.id)
    serializer = serializers.AgeGroupSerializer(filteredAgeGroup, many=True)    
    assert resp.data == serializer.data

def test_getRequestByVendorUser(api_client, vendorUser, ageGroup):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    filteredAgeGroup = AgeGroup.objects.filter(country__id=ageGroup.id)
    serializer = serializers.AgeGroupSerializer(filteredAgeGroup, many=True)    
    assert resp.data == serializer.data

def test_getRequestBySubAdmin(api_client, subAdmin, ageGroup):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    filteredAgeGroup = AgeGroup.objects.filter(country__id=ageGroup.id)
    serializer = serializers.AgeGroupSerializer(filteredAgeGroup, many=True)    
    assert resp.data == serializer.data

def test_getRequestBySuperAdmin(api_client, superAdmin, ageGroup):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    filteredAgeGroup = AgeGroup.objects.filter(country__id=ageGroup.id)
    serializer = serializers.AgeGroupSerializer(filteredAgeGroup, many=True)    
    assert resp.data == serializer.data


def test_postRequestWithoutLogin(api_client, ageGroup):
    resp = api_client.post(url)
    assert resp.status_code == 405

def test_postRequestByUser(api_client, user, ageGroup):
    api_client.force_authenticate(user)
    resp = api_client.post(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_postRequestByVendorUser(api_client, vendorUser, ageGroup):
    api_client.force_authenticate(vendorUser)
    resp = api_client.post(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_postRequestBySubAdmin(api_client, subAdmin, ageGroup):
    api_client.force_authenticate(subAdmin)
    resp = api_client.post(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    

def test_postRequestBySuperAdmin(api_client, superAdmin, ageGroup):
    api_client.force_authenticate(superAdmin)
    resp = api_client.post(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patchRequestWithoutLogin(api_client, ageGroup):
    resp = api_client.patch(url)
    assert resp.status_code == 405

def test_patchRequestByUser(api_client, user, ageGroup):
    api_client.force_authenticate(user)
    resp = api_client.patch(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_patchRequestByVendorUser(api_client, vendorUser, ageGroup):
    api_client.force_authenticate(vendorUser)
    resp = api_client.patch(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patchRequestBySubAdmin(api_client, subAdmin, ageGroup):
    api_client.force_authenticate(subAdmin)
    resp = api_client.patch(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    

def test_patchRequestBySuperAdmin(api_client, superAdmin, ageGroup):
    api_client.force_authenticate(superAdmin)
    resp = api_client.patch(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_deleteRequestWithoutLogin(api_client, ageGroup):
    resp = api_client.delete(url)
    assert resp.status_code == 405

def test_deleteRequestByUser(api_client, user, ageGroup):
    api_client.force_authenticate(user)
    resp = api_client.delete(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_deleteRequestByVendorUser(api_client, vendorUser, ageGroup):
    api_client.force_authenticate(vendorUser)
    resp = api_client.delete(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_deleteRequestBySubAdmin(api_client, subAdmin, ageGroup):
    api_client.force_authenticate(subAdmin)
    resp = api_client.delete(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    

def test_deleteRequestBySuperAdmin(api_client, superAdmin, ageGroup):
    api_client.force_authenticate(superAdmin)
    resp = api_client.delete(url, data={}, format='json')
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


