import pytest
from django.urls import reverse


url = reverse('superadmin:vendor_and_user_management:currentuserfamily')


def test_Request(api_client):
    resp = api_client.get(url)
    assert resp.status_code == 401

    resp = api_client.post(url)
    assert resp.status_code == 401

    resp = api_client.put(url)
    assert resp.status_code == 401

    resp = api_client.patch(url)
    assert resp.status_code == 401

    resp = api_client.delete(url)
    assert resp.status_code == 401


def test_getRequestWithoutFamily(api_client, userDetails, city):
    api_client.force_authenticate(userDetails)
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert resp.data['superadmin']['city'] == city.name
    assert resp.data['superadmin']['email'] == userDetails.email


def test_getRequestWithFamily(api_client, userFamily, city):
    api_client.force_authenticate(userFamily)
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert resp.data['superadmin']['city'] == city.name
    assert resp.data['superadmin']['email'] == userFamily.email


def test_patchRequest(api_client, userFamily):
    data = {
        'status': 'SUSPENDED',
        'superadmin': {'email': 'user2@gmail.com'}
    }

    api_client.force_authenticate(userFamily)
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == 200
    assert resp.data['status'] == data['status']
    assert resp.data['superadmin']['email'] != data['superadmin']['email']


def test_putRequest(api_client, userFamily):
    data = {
        'status': 'SUSPENDED',
        'superadmin': {'email': 'user2@gmail.com'}
    }

    api_client.force_authenticate(userFamily)
    resp = api_client.put(url, data=data, format='json')
    assert resp.status_code == 405

def test_deleteRequest(api_client, userFamily):
    api_client.force_authenticate(userFamily)
    resp = api_client.delete(url)
    assert resp.status_code == 405

# pytest test_currentuserfamily_api.py -s
