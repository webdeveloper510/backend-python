from attr import dataclass
import pytest
from django.urls import reverse
from faker import Faker
import datetime
from superadmin.subapps.media_and_groupings.models import Marketing
from superadmin.subapps.media_and_groupings import serializers_marketing
import datetime

url = reverse('superadmin:media_and_groupings:marketing', kwargs={'id': 1})

now = datetime.datetime.now()
first_day = now.strftime("%Y-%m-%d")
to_day = now + datetime.timedelta(days=1)
to_day = to_day.strftime("%Y-%m-%d")


def test_requestWithoutLogin(api_client, marketing):
    resp = api_client.get(url)
    assert resp.status_code == 200
    all_marketing = Marketing.objects.get(id=1)
    serializer = serializers_marketing.MarketingSerializer(all_marketing)
    assert resp.data == serializer.data
    
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405


def test_patchRequestWithoutLogin(api_client, marketing):
    to_day = now + datetime.timedelta(days=1)
    to_day = to_day.strftime("%Y-%m-%d")
    data = {
        'to_date': to_day
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == 200
    


def test_getRequestByUser(api_client, user, marketing):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all_marketing = Marketing.objects.get(id=1)
    serializer = serializers_marketing.MarketingSerializer(all_marketing)
    assert resp.data == serializer.data


def test_getRequestByVendorUser(api_client, vendorUser, marketing):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all_marketing = Marketing.objects.get(id=1)
    serializer = serializers_marketing.MarketingSerializer(all_marketing)
    assert resp.data == serializer.data


def test_getRequestBySubAdmin(api_client, subAdmin, marketing):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all_marketing = Marketing.objects.get(id=1)
    serializer = serializers_marketing.MarketingSerializer(all_marketing)
    assert resp.data == serializer.data


def test_getRequestBySuperAdmin(api_client, superAdmin, marketing):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all_marketing = Marketing.objects.get(id=1)
    serializer = serializers_marketing.MarketingSerializer(all_marketing)
    assert resp.data == serializer.data



def test_postRequestByVednor(api_client, vendorUser, city, vendor, vendorDetails):
    api_client.force_authenticate(vendorUser)
    # Day Access

    data = {
        'from_date' : first_day,
        'to_date' : to_day,
        

    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 405



def test_postRequestBySubAdmin(api_client, subAdmin, city, vendor, vendorDetails):
    api_client.force_authenticate(subAdmin)
    # Day Access

    data = {
        'from_date' : first_day,
        'to_date' : to_day,
        'type' : 'BANNER',
        

    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 405



def test_postRequestBySuperAdmin(api_client, superAdmin, city, vendor, vendorDetails):
    api_client.force_authenticate(superAdmin)
    # Day Access

    data = {
        'from_date' : first_day,
        'to_date' : to_day,
        'type' : 'BANNER'
    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 405



def test_patchRequestByUser(api_client, user, marketing):
    to_day = now + datetime.timedelta(days=1)
    to_day = to_day.strftime("%Y-%m-%d")
    api_client.force_authenticate(user)
    data = {
        'to_date': to_day
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == 200
