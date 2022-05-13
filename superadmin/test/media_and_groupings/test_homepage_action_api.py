from datetime import datetime
import pytest
from faker import Faker
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_categories
from django.urls import reverse
from rest_framework import status



url = reverse('superadmin:media_and_groupings:homepage_action', kwargs={'id': 1, 'action': 'SUSPEND'})

def test_requestWithoutLogin(api_client, headerDetails, city, category, vendor, vendorUser, vendorDetails):
    resp = api_client.get(url)
    assert resp.status_code == 200
    m_obj = models.Marketing.objects.get(id=1)
    assert m_obj.status == 'SUSPENDED'

    url1 = reverse('superadmin:media_and_groupings:homepage_action', kwargs={'id': 1, 'action': 'ACTIVATE'})
    resp = api_client.get(url1)
    assert resp.status_code == 200
    m_obj = models.Marketing.objects.get(id=1)
    assert m_obj.status == 'ACTIVE'

    url1 = reverse('superadmin:media_and_groupings:homepage_action', kwargs={'id': 1, 'action': 'ACTIVE'})
    resp = api_client.get(url1)
    assert resp.status_code == 400
    
    resp = api_client.post(url)
    assert resp.status_code == 405

    resp = api_client.patch(url)
    assert resp.status_code == 405

    resp = api_client.put(url)
    assert resp.status_code == 405

    resp = api_client.delete(url)
    assert resp.status_code == 405

def test_getRequestBySubAdmin(api_client, subAdmin, headerDetails, city, category, vendor, vendorUser, vendorDetails):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 200
    m_obj = models.Marketing.objects.get(id=1)
    assert m_obj.status == 'SUSPENDED'

    url1 = reverse('superadmin:media_and_groupings:homepage_action', kwargs={'id': 1, 'action': 'ACTIVATE'})
    resp = api_client.get(url1)
    assert resp.status_code == 200
    m_obj = models.Marketing.objects.get(id=1)
    assert m_obj.status == 'ACTIVE'

    url1 = reverse('superadmin:media_and_groupings:homepage_action', kwargs={'id': 1, 'action': 'ACTIVE'})
    resp = api_client.get(url1)
    assert resp.status_code == 400

def test_getRequestBySuperAdmin(api_client, superAdmin, headerDetails, city, category, vendor, vendorUser, vendorDetails):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 200
    m_obj = models.Marketing.objects.get(id=1)
    assert m_obj.status == 'SUSPENDED'

    url1 = reverse('superadmin:media_and_groupings:homepage_action', kwargs={'id': 1, 'action': 'ACTIVATE'})
    resp = api_client.get(url1)
    assert resp.status_code == 200
    m_obj = models.Marketing.objects.get(id=1)
    assert m_obj.status == 'ACTIVE'

    url1 = reverse('superadmin:media_and_groupings:homepage_action', kwargs={'id': 1, 'action': 'ACTIVE'})
    resp = api_client.get(url1)
    assert resp.status_code == 400

def test_getRequestByUser(api_client, user, headerDetails, city, category, vendor, vendorUser, vendorDetails):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 200
    m_obj = models.Marketing.objects.get(id=1)
    assert m_obj.status == 'SUSPENDED'

    url1 = reverse('superadmin:media_and_groupings:homepage_action', kwargs={'id': 1, 'action': 'ACTIVATE'})
    resp = api_client.get(url1)
    assert resp.status_code == 200
    m_obj = models.Marketing.objects.get(id=1)
    assert m_obj.status == 'ACTIVE'

    url1 = reverse('superadmin:media_and_groupings:homepage_action', kwargs={'id': 1, 'action': 'ACTIVE'})
    resp = api_client.get(url1)
    assert resp.status_code == 400

def test_getRequestByvendorUser(api_client, headerDetails, city, category, vendor, vendorUser, vendorDetails):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == 200
    m_obj = models.Marketing.objects.get(id=1)
    assert m_obj.status == 'SUSPENDED'

    url1 = reverse('superadmin:media_and_groupings:homepage_action', kwargs={'id': 1, 'action': 'ACTIVATE'})
    resp = api_client.get(url1)
    assert resp.status_code == 200
    m_obj = models.Marketing.objects.get(id=1)
    assert m_obj.status == 'ACTIVE'

    url1 = reverse('superadmin:media_and_groupings:homepage_action', kwargs={'id': 1, 'action': 'ACTIVE'})
    resp = api_client.get(url1)
    assert resp.status_code == 400
