import pytest
from django.urls import reverse
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_attributes as serializers



url = reverse('superadmin:media_and_groupings:addSubAttributes')


def test_requestWithoutLogin(api_client,attribute, subAttributes):
    resp = api_client.get(url)
    assert resp.status_code == 405
    
    resp = api_client.patch(url)
    assert resp.status_code == 405

    resp = api_client.put(url)
    assert resp.status_code == 405

    
    url1 = reverse('superadmin:media_and_groupings:deleteSubAttributes', kwargs={'sid': 1})
    resp = api_client.delete(url1)
    assert resp.status_code == 204

def test_post_requestWithoutLogin(api_client,attribute):
    resp = api_client.post(url)
    data = {
        'name': attribute.name,
        'subAttribute': [
            {"name": "Sub Attr", 'status': 'ACTIVE'},
            {"name": "Sub Att2", 'status': 'ACTIVE'}
        ]
    }
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    assert resp.data['faildSubAttributes'] == []

    all_sub = models.SubAttribute.objects.all()
    assert len(all_sub) == 2




def test_getRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 405

def test_getRequestByVendorUser(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == 405

def test_getRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 405

def test_getRequestBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 405


def test_putRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.put(url)
    assert resp.status_code == 405

def test_putRequestByVendorUser(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.put(url)
    assert resp.status_code == 405

def test_putRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    resp = api_client.put(url)
    assert resp.status_code == 405

def test_putRequestBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.put(url)
    assert resp.status_code == 405

def test_patchRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.patch(url)
    assert resp.status_code == 405

def test_patchRequestByVendorUser(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.patch(url)
    assert resp.status_code == 405

def test_patchRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    resp = api_client.patch(url)
    assert resp.status_code == 405

def test_patchRequestBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.patch(url)
    assert resp.status_code == 405


def test_deleteRequestByUser(api_client, user, subAttributes):
    api_client.force_authenticate(user)
    url1 = reverse('superadmin:media_and_groupings:deleteSubAttributes', kwargs={'sid': 1})
    resp = api_client.delete(url1)
    assert resp.status_code == 204

def test_deleteRequestByVendorUser(api_client, vendorUser, subAttributes):
    api_client.force_authenticate(vendorUser)
    # resp = api_client.delete(url)
    # assert resp.status_code == 405
    url1 = reverse('superadmin:media_and_groupings:deleteSubAttributes', kwargs={'sid': 1})
    resp = api_client.delete(url1)
    assert resp.status_code == 204

def test_deleteRequestBySubAdmin(api_client, subAdmin, subAttributes):
    api_client.force_authenticate(subAdmin)
    # resp = api_client.delete(url)
    # assert resp.status_code == 405
    url1 = reverse('superadmin:media_and_groupings:deleteSubAttributes', kwargs={'sid': 1})
    resp = api_client.delete(url1)
    assert resp.status_code == 204

def test_deleteRequestBySuperAdmin(api_client, superAdmin, subAttributes):
    api_client.force_authenticate(superAdmin)
    # resp = api_client.delete(url)
    # assert resp.status_code == 405
    url1 = reverse('superadmin:media_and_groupings:deleteSubAttributes', kwargs={'sid': 1})
    resp = api_client.delete(url1)
    assert resp.status_code == 204



def test_postRequestByUser(api_client, user, attribute):
    data = {
        'name': attribute.name,
        'subAttribute': [
            {"name": "Sub Attr", 'status': 'ACTIVE'},
            {"name": "Sub Att2", 'status': 'ACTIVE'}
        ]
    }
    api_client.force_authenticate(user)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    assert resp.data['faildSubAttributes'] == []

    all_sub = models.SubAttribute.objects.all()
    assert len(all_sub) == 2


def test_postRequestByVendorUser(api_client, vendorUser, attribute):
    data = {
        'name': attribute.name,
        'subAttribute': [
            {"name": "Sub Attr", 'status': 'ACTIVE'},
            {"name": "Sub Att2", 'status': 'ACTIVE'}
        ]
    }
    api_client.force_authenticate(vendorUser)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    assert resp.data['faildSubAttributes'] == []

    all_sub = models.SubAttribute.objects.all()
    assert len(all_sub) == 2


def test_postRequestBySubAdmin(api_client, subAdmin, attribute):
    data = {
        'name': attribute.name,
        'subAttribute': [
            {"name": "Sub Attr", 'status': 'ACTIVE'},
            {"name": "Sub Att2", 'status': 'ACTIVE'}
        ]
    }
    api_client.force_authenticate(subAdmin)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    assert resp.data['faildSubAttributes'] == []

    all_sub = models.SubAttribute.objects.all()
    assert len(all_sub) == 2


def test_postRequestBySuperAdmin(api_client, superAdmin, attribute):
    data = {
        'name': attribute.name,
        'subAttribute': [
            {"name": "Sub Attr", 'status': 'ACTIVE'},
            {"name": "Sub Att2", 'status': 'ACTIVE'}
        ]
    }
    api_client.force_authenticate(superAdmin)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    assert resp.data['faildSubAttributes'] == []

    all_sub = models.SubAttribute.objects.all()
    assert len(all_sub) == 2