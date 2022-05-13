from attr import dataclass
import pytest
from django.urls import reverse
from faker import Faker
import datetime
from superadmin.subapps.media_and_groupings.models import Marketing
from superadmin.subapps.media_and_groupings import serializers_marketing
import datetime

url = reverse('superadmin:media_and_groupings:marketings')

now = datetime.datetime.now()
first_day = now.strftime("%Y-%m-%d")
to_day = now + datetime.timedelta(days=1)
to_day = to_day.strftime("%Y-%m-%d")


def test_requestWithoutLogin(api_client, marketing):
    resp = api_client.get(url)
    assert resp.status_code == 200
    all_marketing = Marketing.objects.all()
    serializer = serializers_marketing.MarketingSerializer(all_marketing, many=True)
    assert resp.data == serializer.data

def test_postRequestWithoutLogin(api_client, vendor, city):
    
    data = {
        'from_date' : first_day,
        'to_date' : to_day,
        'type' : 'BANNER',
        'vendor' : vendor.id,
        'target_activity' : 'Day Access',
        'city': city.name,  
        'platform_type' : 'WEB',
        'status' : 'ACTIVE', 
        'total_amount_paid' : 2000,
        'applied_tax_rate': 18,
        'transaction_id' : "2515548KJASF"
    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 201
    market = Marketing.objects.get(id=resp.data['id'])
    serializer = serializers_marketing.MarketingSerializer(market)
    assert resp.data == serializer.data
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    resp = api_client.patch(url)
    assert resp.status_code == 405
    
    resp = api_client.delete(url)
    assert resp.status_code == 405


def test_getRequestByUser(api_client, user, marketing):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all_marketing = Marketing.objects.all()
    serializer = serializers_marketing.MarketingSerializer(all_marketing, many=True)
    assert resp.data == serializer.data


def test_getRequestByVendorUser(api_client, vendorUser, marketing):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all_marketing = Marketing.objects.all()
    serializer = serializers_marketing.MarketingSerializer(all_marketing, many=True)
    assert resp.data == serializer.data


def test_getRequestBySubAdmin(api_client, subAdmin, marketing):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all_marketing = Marketing.objects.all()
    serializer = serializers_marketing.MarketingSerializer(all_marketing, many=True)
    assert resp.data == serializer.data


def test_getRequestBySuperAdmin(api_client, superAdmin, marketing):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all_marketing = Marketing.objects.all()
    serializer = serializers_marketing.MarketingSerializer(all_marketing, many=True)
    assert resp.data == serializer.data



def test_postRequestByVednor(api_client, vendorUser, city, vendor, vendorDetails):
    api_client.force_authenticate(vendorUser)
    # Day Access

    data = {
        'from_date' : first_day,
        'to_date' : to_day,
        'type' : 'BANNER',
        'vendor' : vendor.id,
        'target_activity' : 'Day Access',
        'city': city.name,  
        'platform_type' : 'WEB',
        'status' : 'ACTIVE', 
        'total_amount_paid' : 2000,
        'applied_tax_rate': 18,
        'transaction_id' : "2515548KJASF"

    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 201
    market = Marketing.objects.get(id=resp.data['id'])
    serializer = serializers_marketing.MarketingSerializer(market)
    assert resp.data == serializer.data



def test_postRequestBySubAdmin(api_client, subAdmin, city, vendor, vendorDetails):
    api_client.force_authenticate(subAdmin)
    # Day Access

    data = {
        'from_date' : first_day,
        'to_date' : to_day,
        'type' : 'BANNER',
        'vendor' : vendor.id,
        'target_activity' : 'Day Access',
        'city': city.name,  
        'platform_type' : 'WEB',
        'status' : 'ACTIVE', 
        'total_amount_paid' : 2000,
        'applied_tax_rate': 18,
        'transaction_id' : "2515548KJASF"

    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 201
    market = Marketing.objects.get(id=resp.data['id'])
    serializer = serializers_marketing.MarketingSerializer(market)
    assert resp.data == serializer.data



def test_postRequestBySuperAdmin(api_client, superAdmin, city, vendor, vendorDetails):
    api_client.force_authenticate(superAdmin)
    # Day Access

    data = {
        'from_date' : first_day,
        'to_date' : to_day,
        'type' : 'BANNER',
        'vendor' : vendor.id,
        'target_activity' : 'Day Access',
        'city': city.name,  
        'platform_type' : 'WEB',
        'status' : 'ACTIVE', 
        'total_amount_paid' : 2000,
        'applied_tax_rate': 18,
        'transaction_id' : "2515548KJASF"
    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 201
    market = Marketing.objects.get(id=resp.data['id'])
    serializer = serializers_marketing.MarketingSerializer(market)
    assert resp.data == serializer.data


def test_RequestByUser(api_client, user, marketing):
    api_client.force_authenticate(user)
    data= {}
    resp = api_client.put(url, data)
    assert resp.status_code == 405
    
    resp = api_client.patch(url, data)
    assert resp.status_code == 405

    resp = api_client.delete(url, data)
    assert resp.status_code == 405

def test_RequestByVendorUser(api_client, vendorUser, marketing):
    api_client.force_authenticate(vendorUser)
    data= {}
    resp = api_client.put(url, data)
    assert resp.status_code == 405
    
    resp = api_client.patch(url, data)
    assert resp.status_code == 405

    resp = api_client.delete(url, data)
    assert resp.status_code == 405

def test_RequestByVendorSubAdmin(api_client, subAdmin, marketing):
    api_client.force_authenticate(subAdmin)
    data= {}
    resp = api_client.put(url, data)
    assert resp.status_code == 405
    
    resp = api_client.patch(url, data)
    assert resp.status_code == 405

    resp = api_client.delete(url, data)
    assert resp.status_code == 405


def test_RequestByVendorSuperAdmin(api_client, superAdmin, marketing):
    api_client.force_authenticate(superAdmin)
    data= {}
    resp = api_client.put(url, data)
    assert resp.status_code == 405
    
    resp = api_client.patch(url, data)
    assert resp.status_code == 405

    resp = api_client.delete(url, data)
    assert resp.status_code == 405

