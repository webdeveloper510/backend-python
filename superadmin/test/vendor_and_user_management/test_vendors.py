from django.urls.base import reverse
import pytest
from django.urls import reverse
from superadmin.subapps.vendor_and_user_management.models import Vendor
from superadmin.subapps.vendor_and_user_management.serializers import VendorSerializer

url = reverse("superadmin:vendor_and_user_management:Vendors")


def test_getVendors(api_client, vendor, vendorDetails):
    resp = api_client.get(url)
    assert resp.status_code == 200
    all_vendor = Vendor.objects.all()
    serializer = VendorSerializer(all_vendor, many=True)
    assert serializer.data == resp.data

    urlWithPageination = url + '?perpage=10'
    resp = api_client.get(urlWithPageination)
    assert resp.status_code == 200
    assert resp.data['count'] == 1
    assert resp.data['next'] == None
    assert resp.data['previous'] == None
    assert len(resp.data['results']) == 1
    assert resp.data['results'] == serializer.data

    urlWithCountry = url + '?country=India'
    resp = api_client.get(urlWithCountry)
    assert resp.status_code == 200
    assert len(resp.data) == 1


def test_postRequest(api_client, vendor, vendorDetails, country, city):
    data = {
        "username": "vendor1",
        "password": "testuser",
        "name": "Jon Doe",
        "email": "vendor3@email.com",
        "country": country.name,
        "city": city.name,
        "vendor_status": "ACTIVE",
        "organization_type": "INDIVIDUAL",
        "legal_name": "Legal Name",
        "code": "S1",
        "entity_reg_number": "11111222",
        "logo": None,
        "media": [{
            "id": 144,
            "name": "CATEGORY_ICON",
            "file": 'data:image/webp;base64,UklGRl4DAABXRUJQVlA4WAoAAAAwAAAAIwAAIwAASUNDUBgCAAAAAAIYAAAAAAIQAABtbnRyUkdCIFhZWiAAAAAAAAAAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAAHRyWFlaAAABZAAAABRnWFlaAAABeAAAABRiWFlaAAABjAAAABRyVFJDAAABoAAAAChnVFJDAAABoAAAAChiVFJDAAABoAAAACh3dHB0AAAByAAAABRjcHJ0AAAB3AAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAFgAAAAcAHMAUgBHAEIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFhZWiAAAAAAAABvogAAOPUAAAOQWFlaIAAAAAAAAGKZAAC3hQAAGNpYWVogAAAAAAAAJKAAAA+EAAC2z3BhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABYWVogAAAAAAAA9tYAAQAAAADTLW1sdWMAAAAAAAAAAQAAAAxlblVTAAAAIAAAABwARwBvAG8AZwBsAGUAIABJAG4AYwAuACAAMgAwADEANkFMUEjuAAAABYBjbdsx5xmzn/af2YE6I0ltYxW2nVXYKu10WkKmTW/j0/tFdUQwcNu2kWq1t6/rFfiREozi9FIT12QpgOX6ey0Wy7gvLZWTyI/YGd4GvM2i2oyJG8bT2baMqVpJF6brVL2QHG9BhawbBeJh65AE/kRG27BAd4/G5PX0/gl2AgF9Ngt9+34VFB+QPFBB0tg3VBBVXiZKIneVVqiGmb7eyJdKI30A50aBTGqVg3PjXSbhshhwUveAGDDJ+0QMk76XxOBTjf0mBsb37NsfpXVIg7ZhgfwtDQq2xR5M1ZKZrvvqg3gYsZN4Ovs8/pcKAFZQOCAqAAAAMAMAnQEqJAAkAD5tNphIpCMioSOIAIANiWkAABuBvT4OAAD++5zAAAAA'
            }],
        "profile_intro": "intro 11",
        "terms": "terms 11",
        "website": "https://google.com",
        "video_introduction_url": "https://google.com",
        "registered_address": {
            "address_line_1": "line 11",
            "address_line_2": "line 22",
            "phone_office": "544533",
            "phone_mobile": "123144",
            "zipcode": 5555
        },
        "mailing_address": {
            "address_line_1": "line 1199",
            "address_line_2": "lline 2288",
            "phone_office": "48794699",
            "phone_mobile": "3856377",
            "zipcode": 4444
        }
    }

    resp = api_client.post(url, data=data, format='json')
    # print(resp.data)
    assert resp.status_code == 201
    vendor = Vendor.objects.get(id=2)
    serializer = VendorSerializer(vendor)

    assert resp.data == serializer.data


def test_patchRequest(api_client, vendor, vendorDetails):
    data = {
        "status": "SUSPENDED"
    }
    resp = api_client.patch(url, data=data)
    assert resp.status_code == 405


def test_putRequest(api_client, vendor, vendorDetails):
    data = {
        "status": "SUSPENDED"
    }
    resp = api_client.put(url, data=data)
    assert resp.status_code == 405


def test_deleteRequest(api_client, vendor, vendorDetails):
    data = {
        "status": "SUSPENDED"
    }
    resp = api_client.delete(url, data=data)
    assert resp.status_code == 405


# pytest test_vendors.py -s
