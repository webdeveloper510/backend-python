import pytest
from django.urls import reverse
from faker import Faker
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_avatars as serializers


url = reverse('superadmin:media_and_groupings:avatar', kwargs={'id': 1})

def test_getRequest(api_client, avatars):
    resp = api_client.get(url)
    assert resp.status_code == 405



def test_getByUserRequest(api_client, user, avatars):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 405


def test_getRequestByVendor(api_client, vendorUser, avatars):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == 405

def test_getRequestbySuperAdmin(api_client, superAdmin, avatars):

    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 405

@pytest.mark.django_db
def test_postRequest(api_client, avatar):
    resp = api_client.patch(url)
    assert resp.status_code == 405

    

@pytest.mark.django_db
def test_postRequestBySuperAdmin(api_client, superAdmin, avatar):
    api_client.force_authenticate(superAdmin)
    resp = api_client.patch(url)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_postRequestByVendor(api_client, vendor, avatar):
    api_client.force_authenticate(vendor)
    resp = api_client.patch(url)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_postRequestByUser(api_client, user, avatar):
    api_client.force_authenticate(user)
    resp = api_client.patch(url)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_patchRequest(api_client, db, avatar):
    resp = api_client.patch(url)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_patchRequestByUser(api_client, user,db, avatar):
    api_client.force_authenticate(user)
    resp = api_client.patch(url)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_patchRequestByVendor(api_client, vendor, db, avatar):
    api_client.force_authenticate(vendor)
    resp = api_client.patch(url)
    assert resp.status_code == 405

@pytest.mark.django_db
def test_patchRequestBySuperAdmin(api_client, superAdmin, avatar, db):
    api_client.force_authenticate(superAdmin)
    resp = api_client.patch(url)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_putRequest(api_client, db, avatar):
    resp = api_client.put(url)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_putRequestByUser(api_client, user, avatar, db):
    api_client.force_authenticate(user)
    resp = api_client.put(url)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_putRequestByVendor(api_client, vendor, db, avatar):
    api_client.force_authenticate(vendor)
    resp = api_client.put(url)
    assert resp.status_code == 405

@pytest.mark.django_db
def test_putRequestBySuperAdmin(api_client, superAdmin, db, avatar):
    api_client.force_authenticate(superAdmin)
    resp = api_client.put(url)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_deleteRequest(api_client, db, avatar):
    resp = api_client.delete(url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_deleteRequestByUser(api_client, user,db, avatar):
    api_client.force_authenticate(user)
    resp = api_client.delete(url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_deleteRequestByVendor(api_client, vendor, db, avatar):
    api_client.force_authenticate(vendor)
    resp = api_client.delete(url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_deleteRequestBySuperAdmin(api_client, superAdmin, db, avatar):
    api_client.force_authenticate(superAdmin)
    resp = api_client.delete(url)
    assert resp.status_code == 200


# pytest test_avatar_api.py -s


