import pytest
from faker import Faker
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_categories
from django.urls import reverse
from rest_framework import status


url = reverse('superadmin:media_and_groupings:subcategories')

def test_getRequestWithoutLogin(api_client):
    resp = api_client.get(url)
    assert resp.status_code == 405

def test_postRequestWithoutLogin(api_client, category):
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.post(url, data=data, format="json")
    assert resp.status_code == status.HTTP_201_CREATED
    all_sub = models.SubCategory.objects.all()
    assert len(all_sub) == 2
    
    firstCat = all_sub.first()
    assert firstCat.status == 'INACTIVE'

def test_patchRequestWithoutLogin(api_client):
    resp = api_client.patch(url)
    assert resp.status_code == 405

def test_putRequestWithoutLogin(api_client):
    resp = api_client.put(url)
    assert resp.status_code == 405

def test_deleteRequestWithoutLogin(api_client, category):
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.delete(url, data=data, format="json")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_getRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_getRequestByVendorUser(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_getRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_getRequestBySuperUser(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestByVendorUser(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestBySuperUser(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_postRequestByUser(api_client, user, category):
    api_client.force_authenticate(user)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.post(url, data=data, format="json")
    assert resp.status_code == status.HTTP_201_CREATED
    all_sub = models.SubCategory.objects.all()
    assert len(all_sub) == 2
    
    firstCat = all_sub.first()
    assert firstCat.status == 'INACTIVE'

def test_postRequestByVendorUser(api_client, vendorUser, category):
    api_client.force_authenticate(vendorUser)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.post(url, data=data, format="json")
    assert resp.status_code == status.HTTP_201_CREATED
    all_sub = models.SubCategory.objects.all()
    assert len(all_sub) == 2
    
    firstCat = all_sub.first()
    assert firstCat.status == 'INACTIVE'

def test_postRequestBySubAdmin(api_client, subAdmin, category):
    api_client.force_authenticate(subAdmin)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.post(url, data=data, format="json")
    assert resp.status_code == status.HTTP_201_CREATED
    all_sub = models.SubCategory.objects.all()
    assert len(all_sub) == 2
    
    firstCat = all_sub.first()
    assert firstCat.status == 'INACTIVE'

def test_postRequestBySuperAdmin(api_client, superAdmin, category):
    api_client.force_authenticate(superAdmin)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.post(url, data=data, format="json")
    assert resp.status_code == status.HTTP_201_CREATED
    all_sub = models.SubCategory.objects.all()
    assert len(all_sub) == 2

    firstCat = all_sub.first()
    assert firstCat.status == 'INACTIVE'

def test_postRequestBySuperAdmin(api_client, superAdmin, category):
    api_client.force_authenticate(superAdmin)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.post(url, data=data, format="json")
    assert resp.status_code == status.HTTP_201_CREATED
    all_sub = models.SubCategory.objects.all()
    assert len(all_sub) == 2

    firstCat = all_sub.first()
    assert firstCat.status == 'INACTIVE'

def test_patchRequestBySuperAdmin(api_client, superAdmin, category):
    api_client.force_authenticate(superAdmin)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_patchRequestBySubAdmin(api_client, subAdmin, category):
    api_client.force_authenticate(subAdmin)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_patchRequestByVendorUser(api_client, vendorUser, category):
    api_client.force_authenticate(vendorUser)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patchRequestByUser(api_client, user, category):
    api_client.force_authenticate(user)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestBySuperAdmin(api_client, superAdmin, category):
    api_client.force_authenticate(superAdmin)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.put(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestBySubAdmin(api_client, subAdmin, category):
    api_client.force_authenticate(subAdmin)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.put(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_putRequestByVendorUser(api_client, vendorUser, category):
    api_client.force_authenticate(vendorUser)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.put(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_putRequestByUser(api_client, user, category):
    api_client.force_authenticate(user)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.put(url, data=data, format="json")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_deleteRequestBySuperAdmin(api_client, superAdmin, category):
    api_client.force_authenticate(superAdmin)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.delete(url, data=data, format="json")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_deleteRequestBySubAdmin(api_client, subAdmin, category):
    api_client.force_authenticate(subAdmin)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.delete(url, data=data, format="json")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_deleteRequestByVendorUser(api_client, vendorUser, category):
    api_client.force_authenticate(vendorUser)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.delete(url, data=data, format="json")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_deleteRequestByUser(api_client, user, category):
    api_client.force_authenticate(user)
    data = {
        'name': category.name,
        "subCategory": [
            {"name":"SubCate2"},
            {"name":"SubCate3"}
        ]
    }
    resp = api_client.delete(url, data=data, format="json")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

