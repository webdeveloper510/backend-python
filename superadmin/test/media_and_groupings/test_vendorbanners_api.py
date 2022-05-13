from datetime import datetime
import pytest
from faker import Faker
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_categories
from django.urls import reverse



url = reverse('superadmin:media_and_groupings:vendorbanners')

def test_requestsWithoutLogin(api_client, bannerDetails, city, category, vendor, vendorUser, vendorDetails):
    now = datetime.now()
    first_day = now.strftime("%Y-%m-%d")
    url1 = url + '?first_date='+ first_day + "&last_date="+first_day + "&platform_type=WEB&city=" + city.name + '&catagory='+ str(category.name)
    resp = api_client.get(url1)
    assert resp.status_code == 200
    
    resp = api_client.post(url)
    assert resp.status_code == 405
    
    resp = api_client.put(url)
    assert resp.status_code == 405

    resp = api_client.patch(url)
    assert resp.status_code == 405

    resp = api_client.delete(url)
    assert resp.status_code == 405


def test_getBannersByUser(api_client, user, bannerDetails, city, category, vendor, vendorUser, vendorDetails):
    api_client.force_authenticate(user)
    now = datetime.now()
    first_day = now.strftime("%Y-%m-%d")
    url1 = url + '?first_date='+ first_day + "&last_date="+first_day + "&platform_type=WEB&city=" + city.name + '&catagory='+ str(category.name)
    resp = api_client.get(url1)
    assert resp.status_code == 200
    


def test_getBannersByVendorUser(api_client, bannerDetails, city, category, vendor, vendorUser, vendorDetails):
    api_client.force_authenticate(vendorUser)
    now = datetime.now()
    first_day = now.strftime("%Y-%m-%d")
    url1 = url + '?first_date='+ first_day + "&last_date="+first_day + "&platform_type=WEB&city=" + city.name + '&catagory='+ str(category.name)
    resp = api_client.get(url1)
    assert resp.status_code == 200
    


def test_getBannersBySubAdmin(api_client, subAdmin, bannerDetails, city, category, vendor, vendorUser, vendorDetails):
    api_client.force_authenticate(subAdmin)
    now = datetime.now()
    first_day = now.strftime("%Y-%m-%d")
    url1 = url + '?first_date='+ first_day + "&last_date="+first_day + "&platform_type=WEB&city=" + city.name + '&catagory='+ str(category.name)
    resp = api_client.get(url1)
    assert resp.status_code == 200
    


def test_getBannersBySuperAdmin(api_client, superAdmin, bannerDetails, city, category, vendor, vendorUser, vendorDetails):
    api_client.force_authenticate(superAdmin)
    now = datetime.now()
    first_day = now.strftime("%Y-%m-%d")
    url1 = url + '?first_date='+ first_day + "&last_date="+first_day + "&platform_type=WEB&city=" + city.name + '&catagory='+ str(category.name)
    resp = api_client.get(url1)
    assert resp.status_code == 200
    
