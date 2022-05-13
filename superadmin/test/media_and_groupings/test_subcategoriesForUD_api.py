import pytest
from faker import Faker
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_categories
from django.urls import reverse
from rest_framework import status


url = reverse('superadmin:media_and_groupings:subcategoriesForUD', kwargs={'sid': 1})

def test_getRequestWithoutLogin(api_client, subCategory):
    resp = api_client.get(url)
    assert resp.status_code == 405

def test_postRequestWithoutLogin(api_client, subCategory):
    resp = api_client.post(url)
    assert resp.status_code == 405

def test_patchRequestWithoutLogin(api_client, subCategory):
    resp = api_client.patch(url)
    assert resp.status_code == 405

def test_putRequestWithoutLogin(api_client, subCategory):
    resp = api_client.put(url)
    assert resp.status_code == 405

def test_deleteRequestWithoutLogin(api_client,category, subCategory):
    resp = api_client.delete(url)
    assert resp.status_code == 204

def test_getRequestByUser(api_client, user, subCategory):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_getRequestByVendorUser(api_client, vendorUser, subCategory):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_getRequestBySubAdmin(api_client, subAdmin, subCategory):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_getRequestBySuperUser(api_client, superAdmin, subCategory):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_postRequestByUser(api_client, user, subCategory):
    api_client.force_authenticate(user)
    resp = api_client.post(url)
    assert resp.status_code == 405

def test_postRequestByVendorUser(api_client, vendorUser, subCategory):
    api_client.force_authenticate(vendorUser)
    resp = api_client.post(url)
    assert resp.status_code == 405

def test_postRequestBySubAdmin(api_client, subAdmin, category, subCategory):
    api_client.force_authenticate(subAdmin)
    data = {
        'no': category.id,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.post(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_postRequestBySuperAdmin(api_client, superAdmin, category, subCategory):
    api_client.force_authenticate(superAdmin)
    data = {
        'no': category.id,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.post(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patchRequestBySuperAdmin(api_client, superAdmin, category, subCategory):
    api_client.force_authenticate(superAdmin)
    data = {
        'no': category.id,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_patchRequestBySubAdmin(api_client, subAdmin, category, subCategory):
    api_client.force_authenticate(subAdmin)
    data = {
        'no': category.id,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_patchRequestByVendorUser(api_client, vendorUser, category, subCategory):
    api_client.force_authenticate(vendorUser)
    data = {
        'no': category.id,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patchRequestByUser(api_client, user, category, subCategory):
    api_client.force_authenticate(user)
    data = {
        'no': category.id,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestBySuperAdmin(api_client, superAdmin, category, subCategory):
    api_client.force_authenticate(superAdmin)
    data = {
        'no': category.id,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.put(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestBySubAdmin(api_client, subAdmin, category, subCategory):
    api_client.force_authenticate(subAdmin)
    data = {
        'no': category.id,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.put(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestByVendorUser(api_client, vendorUser, category, subCategory):
    api_client.force_authenticate(vendorUser)
    data = {
        'no': category.id,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.put(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_putRequestByUser(api_client, user, category, subCategory):
    api_client.force_authenticate(user)
    data = {
        'no': category.id,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.put(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_deleteRequestBySuperAdmin(api_client, superAdmin, category, subCategory):
    api_client.force_authenticate(superAdmin)
    resp = api_client.delete(url)
    assert resp.status_code == 204

def test_deleteRequestBySubAdmin(api_client, subAdmin, category, subCategory):
    api_client.force_authenticate(subAdmin)
    resp = api_client.delete(url)
    assert resp.status_code == 204

def test_deleteRequestByVendorUser(api_client, vendorUser, category, subCategory):
    api_client.force_authenticate(vendorUser)
    resp = api_client.delete(url)
    assert resp.status_code == 204


def test_deleteRequestByUser(api_client, user, category, subCategory):
    api_client.force_authenticate(user)
    resp = api_client.delete(url)
    assert resp.status_code == 204

