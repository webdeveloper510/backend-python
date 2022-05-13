import pytest
from django.urls import reverse
from superadmin.subapps.vendor_and_user_management.models import Vendor
from superadmin.subapps.vendor_and_user_management.serializers import VendorSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


url = reverse(
    "superadmin:vendor_and_user_management:Vendordetails", kwargs={'id': 1})


def test_getVendorDetails(api_client, vendor, country, city, vendorDetails):
    resp = api_client.get(url)
    serializer = VendorSerializer(vendor)
    assert resp.status_code == 200
    assert resp.data == serializer.data


def test_postRequest(api_client, vendor, country, city, vendorDetails):
    data = {}
    resp = api_client.post(url, data=data)
    assert resp.status_code == 405


def test_patchRequest(api_client, vendor, country, city, vendorDetails):
    data = {
        "username": "vendor1",
        "name": "Jon Doe",
        "email": "vendor34@email.com",
        "vendor_status": "ACTIVE",
        "organization_type": "INDIVIDUAL",
        "legal_name": "Legal Name",
        "code": "S1",
        "entity_reg_number": "11111222",
        "logo": None,
        "profile_intro": "intro 11",
        "terms": "terms 12",
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
        },

    }

    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == 200
    vendor = Vendor.objects.get(id=1)
    serialzier = VendorSerializer(vendor)
    assert serialzier.data == resp.data


def test_deleteRequest(api_client, vendor, country, city, vendorDetails):
    resp = api_client.delete(url)
    assert resp.status_code == 200
    all_vendor = Vendor.objects.all()
    assert len(all_vendor) == 0
    all_user = User.objects.all()
    assert len(all_user) == 0


# pytest test_Vendordetails_api.py -s
