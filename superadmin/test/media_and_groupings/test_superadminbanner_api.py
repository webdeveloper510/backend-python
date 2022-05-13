from datetime import datetime
import pytest
from faker import Faker
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_marketing
from django.urls import reverse

url = reverse('superadmin:media_and_groupings:superadminbanner', kwargs={'id': 1})

def test_getRequestWithoutLogin(api_client, city, category, defaultBanner):
    
    resp = api_client.get(url)
    assert resp.status_code == 405

    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    resp = api_client.patch(url)
    assert resp.status_code == 405
    
    resp = api_client.delete(url)
    assert resp.status_code == 204
    url1 = reverse('superadmin:media_and_groupings:superadminbanner', kwargs={'id': 10})
    resp = api_client.delete(url)
    assert resp.status_code == 404

def test_deleteBySubAdmin(api_client, subAdmin, city, category, defaultBanner):
    api_client.force_authenticate(subAdmin)
    resp = api_client.delete(url)
    assert resp.status_code == 204
    url1 = reverse('superadmin:media_and_groupings:superadminbanner', kwargs={'id': 10})
    resp = api_client.delete(url)
    assert resp.status_code == 404

def test_deleteBySuperAdmin(api_client, superAdmin, city, category, defaultBanner):
    api_client.force_authenticate(superAdmin)
    resp = api_client.delete(url)
    assert resp.status_code == 204
    url1 = reverse('superadmin:media_and_groupings:superadminbanner', kwargs={'id': 10})
    resp = api_client.delete(url)
    assert resp.status_code == 404

def test_deleteByvendorUser(api_client, vendorUser, city, category, defaultBanner):
    api_client.force_authenticate(vendorUser)
    resp = api_client.delete(url)
    assert resp.status_code == 204
    url1 = reverse('superadmin:media_and_groupings:superadminbanner', kwargs={'id': 10})
    resp = api_client.delete(url)
    assert resp.status_code == 404

def test_deleteByUser(api_client, user, city, category, defaultBanner):
    api_client.force_authenticate(user)
    resp = api_client.delete(url)
    assert resp.status_code == 204
    url1 = reverse('superadmin:media_and_groupings:superadminbanner', kwargs={'id': 10})
    resp = api_client.delete(url)
    assert resp.status_code == 404

def test_otherRequestByUser(api_client, user, city, category, defaultBanner):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 405
    
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    resp = api_client.patch(url)
    assert resp.status_code == 405
    

def test_otherRequestByvendorUser(api_client, vendorUser, city, category, defaultBanner):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == 405
    
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    resp = api_client.patch(url)
    assert resp.status_code == 405
    

def test_otherRequestBySubAdmin(api_client, subAdmin, city, category, defaultBanner):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 405
    
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    resp = api_client.patch(url)
    assert resp.status_code == 405

def test_otherRequestBySuperAdmin(api_client, superAdmin, city, category, defaultBanner):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 405
    
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    resp = api_client.patch(url)
    assert resp.status_code == 405
    
