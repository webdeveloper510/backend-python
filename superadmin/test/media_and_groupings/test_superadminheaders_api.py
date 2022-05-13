from datetime import datetime
import pytest
from faker import Faker
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_marketing
from django.urls import reverse

fake = Faker()

url = reverse('superadmin:media_and_groupings:superadminheaders')
now = datetime.now()
first_day = now.strftime("%Y-%m-%d")

def test_getRequestWithoutLogin(api_client, city, category, defaultHeader):
    
    url1 = url + "?platform_type=WEB&city="+ city.name + '&first_date='+first_day + '&last_date='+first_day
    resp = api_client.get(url1)
    assert resp.status_code == 200

def test_postRequestWithoutLogin(api_client, city):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    data = {
        "platform_type": "WEB",
        "city": city.name,
        'text': fake.text(),
        'date': today
    }
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    admin_banner = models.DefaultHeader.objects.all().first()
    serializer = serializers_marketing.SuperAdminHomepageHeaderSerializer(admin_banner)
    assert resp.data == serializer.data

    del data['platform_type']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400

    data['platform_type']='WEB'

    
    del data['city']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400

    data['city'] =city.name
    
    resp = api_client.put(url)
    assert resp.status_code == 405
    
    resp = api_client.patch(url)
    assert resp.status_code == 405
    
    resp = api_client.delete(url)
    assert resp.status_code == 405


def test_getRequestByUser(api_client, user, city, category, defaultHeader):
    api_client.force_authenticate(user)
    url1 = url + "?platform_type=WEB&city="+ city.name + '&first_date='+first_day + '&last_date='+first_day
    resp = api_client.get(url1)
    assert resp.status_code == 200


def test_getRequestByVendorUser(api_client, vendorUser, city, category, defaultHeader):
    api_client.force_authenticate(vendorUser)
    url1 = url + "?platform_type=WEB&city="+ city.name + '&first_date='+first_day + '&last_date='+first_day
    resp = api_client.get(url1)
    assert resp.status_code == 200

def test_getRequestBySubAdmin(api_client, subAdmin, city, category, defaultHeader):
    api_client.force_authenticate(subAdmin)
    url1 = url + "?platform_type=WEB&city="+ city.name + '&first_date='+first_day + '&last_date='+first_day
    resp = api_client.get(url1)
    assert resp.status_code == 200

def test_getRequestBySuperAdmin(api_client, superAdmin, city, category, defaultHeader):
    api_client.force_authenticate(superAdmin)
    url1 = url + "?platform_type=WEB&city="+ city.name + '&first_date='+first_day + '&last_date='+first_day
    resp = api_client.get(url1)
    assert resp.status_code == 200


def test_postRequestBySuperAdmin(api_client, superAdmin, city, category):
    api_client.force_authenticate(superAdmin)
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    data = {
        "platform_type": "WEB",
        "city": city.name,
        'text': fake.text(),
        'date': today
    }
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    admin_banner = models.DefaultHeader.objects.all().first()
    serializer = serializers_marketing.SuperAdminHomepageHeaderSerializer(admin_banner)
    assert resp.data == serializer.data

    del data['platform_type']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400

    data['platform_type']='WEB'

    
    del data['city']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400

    data['city'] =city.name
    

def test_postRequestBySubAdmin(api_client, subAdmin, city, category):
    api_client.force_authenticate(subAdmin)
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    data = {
        "platform_type": "WEB",
        "city": city.name,
        'text': fake.text(),
        'date': today
    }
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    admin_banner = models.DefaultHeader.objects.all().first()
    serializer = serializers_marketing.SuperAdminHomepageHeaderSerializer(admin_banner)
    assert resp.data == serializer.data

    del data['platform_type']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400

    data['platform_type']='WEB'

    del data['city']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400

    data['city'] =city.name

def test_postRequestByUser(api_client, user, city, category):
    api_client.force_authenticate(user)
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    data = {
        "platform_type": "WEB",
        "city": city.name,
        'text': fake.text(),
        'date': today
    }
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    admin_banner = models.DefaultHeader.objects.all().first()
    serializer = serializers_marketing.SuperAdminHomepageHeaderSerializer(admin_banner)
    assert resp.data == serializer.data

    del data['platform_type']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400

    data['platform_type']='WEB'

    del data['city']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400

    data['city'] =city.name

def test_postRequestByVendorUser(api_client, vendorUser, city, category):
    api_client.force_authenticate(vendorUser)
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    data = {
        "platform_type": "WEB",
        "city": city.name,
        'text': fake.text(),
        'date': today
    }
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    admin_banner = models.DefaultHeader.objects.all().first()
    serializer = serializers_marketing.SuperAdminHomepageHeaderSerializer(admin_banner)
    assert resp.data == serializer.data

    del data['platform_type']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400

    data['platform_type']='WEB'

    del data['city']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400

    data['city'] =city.name

def test_putByVendorUser(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    data={}
    resp = api_client.put(url, data)    
    assert resp.status_code == 405

def test_putByUser(api_client, user):
    api_client.force_authenticate(user)
    data={}
    resp = api_client.put(url, data)    
    assert resp.status_code == 405

def test_putBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    data={}
    resp = api_client.put(url, data)    
    assert resp.status_code == 405

def test_putBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    data={}
    resp = api_client.put(url, data)    
    assert resp.status_code == 405

def test_patchByVendorUser(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    data={}
    resp = api_client.patch(url, data)    
    assert resp.status_code == 405

def test_patchByUser(api_client, user):
    api_client.force_authenticate(user)
    data={}
    resp = api_client.patch(url, data)    
    assert resp.status_code == 405

def test_patchBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    data={}
    resp = api_client.patch(url, data)    
    assert resp.status_code == 405

def test_patchBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    data={}
    resp = api_client.patch(url, data)    
    assert resp.status_code == 405

def test_deleteByVendorUser(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    data={}
    resp = api_client.delete(url, data)    
    assert resp.status_code == 405

def test_deleteByUser(api_client, user):
    api_client.force_authenticate(user)
    data={}
    resp = api_client.delete(url, data)    
    assert resp.status_code == 405

def test_deleteBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    data={}
    resp = api_client.delete(url, data)    
    assert resp.status_code == 405

def test_deleteBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    data={}
    resp = api_client.delete(url, data)    
    assert resp.status_code == 405