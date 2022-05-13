from datetime import datetime
import pytest
from faker import Faker
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_marketing
from django.urls import reverse

url = reverse('superadmin:media_and_groupings:superadminheader', kwargs={'id': 1})

def test_getRequestWithoutLogin(api_client, city, category, defaultHeader):
    
    resp = api_client.get(url)
    assert resp.status_code == 405

    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    data = {
        'text': 'Other text'
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == 200
    admin_header = models.DefaultHeader.objects.get(id=1)
    assert admin_header.text == 'Other text'
    
    resp = api_client.delete(url)
    assert resp.status_code == 204
    url1 = reverse('superadmin:media_and_groupings:superadminbanner', kwargs={'id': 10})
    resp = api_client.delete(url)
    assert resp.status_code == 404

def test_deleteBySubAdmin(api_client, subAdmin, city, category, defaultHeader):
    api_client.force_authenticate(subAdmin)
    resp = api_client.delete(url)
    assert resp.status_code == 204
    url1 = reverse('superadmin:media_and_groupings:superadminbanner', kwargs={'id': 10})
    resp = api_client.delete(url)
    assert resp.status_code == 404

def test_deleteBySuperAdmin(api_client, superAdmin, city, category, defaultHeader):
    api_client.force_authenticate(superAdmin)
    resp = api_client.delete(url)
    assert resp.status_code == 204
    url1 = reverse('superadmin:media_and_groupings:superadminbanner', kwargs={'id': 10})
    resp = api_client.delete(url)
    assert resp.status_code == 404

def test_deleteByvendorUser(api_client, vendorUser, city, category, defaultHeader):
    api_client.force_authenticate(vendorUser)
    resp = api_client.delete(url)
    assert resp.status_code == 204
    url1 = reverse('superadmin:media_and_groupings:superadminbanner', kwargs={'id': 10})
    resp = api_client.delete(url)
    assert resp.status_code == 404

def test_deleteByUser(api_client, user, city, category, defaultHeader):
    api_client.force_authenticate(user)
    resp = api_client.delete(url)
    assert resp.status_code == 204
    url1 = reverse('superadmin:media_and_groupings:superadminbanner', kwargs={'id': 10})
    resp = api_client.delete(url)
    assert resp.status_code == 404

def test_otherRequestByUser(api_client, user, city, category, defaultHeader):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 405
    
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    

def test_otherRequestByvendorUser(api_client, vendorUser, city, category, defaultHeader):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == 405
    
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    

def test_otherRequestBySubAdmin(api_client, subAdmin, city, category, defaultHeader):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 405
    
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    

def test_otherRequestBySuperAdmin(api_client, superAdmin, city, category, defaultHeader):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 405
    
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    
def test_patchRequestBySuperAdmin(api_client, superAdmin, city, category, defaultHeader):
    api_client.force_authenticate(superAdmin)
    data = {
        'text': 'Other text'
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == 200
    admin_header = models.DefaultHeader.objects.get(id=1)
    assert admin_header.text == 'Other text'
    
    
def test_patchRequestBySubAdmin(api_client, subAdmin, city, category, defaultHeader):
    api_client.force_authenticate(subAdmin)
    data = {
        'text': 'Other text'
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == 200
    admin_header = models.DefaultHeader.objects.get(id=1)
    assert admin_header.text == 'Other text'
    
def test_patchRequestByVendorUser(api_client, vendorUser, city, category, defaultHeader):
    api_client.force_authenticate(vendorUser)
    data = {
        'text': 'Other text'
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == 200
    admin_header = models.DefaultHeader.objects.get(id=1)
    assert admin_header.text == 'Other text'
    
def test_patchRequestByUser(api_client, user, city, category, defaultHeader):
    api_client.force_authenticate(user)
    data = {
        'text': 'Other text'
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == 200
    admin_header = models.DefaultHeader.objects.get(id=1)
    assert admin_header.text == 'Other text'

