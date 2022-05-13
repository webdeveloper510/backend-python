import pytest
from django.urls import reverse

url = reverse('superadmin:vendor_and_user_management:userdetails',
              kwargs={'id': 1})


def test_getRequest(api_client, user, userKids, city, country):
    resp = api_client.get(url)
    assert resp.status_code == 200
    data = resp.data
    assert data['first_name'] == ''
    assert data['last_name'] == ''
    assert data['email'] == user.email
    assert data['city'] == city.name
    assert data['country'] == city.country.name


def test_patchRequest(api_client, user, userKids, city, country):
    data = {
        'first_name': 'john',
        'last_name': 'doe'
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == 200
    assert resp.data['first_name'] == data['first_name']
    assert resp.data['last_name'] == data['last_name']

    data['email'] = 'newEmail@gmail.com'
    resp = api_client.patch(url, data=data, format='json')
    assert resp.data['email'] == data['email']


def test_postRequest(api_client, userKids):

    resp = api_client.post(url, data={}, format='json')
    assert resp.status_code == 405


def test_putRequest(api_client, userKids):
    resp = api_client.put(url, data={}, format='json')
    assert resp.status_code == 405


def test_deleteRequest(api_client, userKids):
    resp = api_client.delete(url, format='json')
    assert resp.status_code == 200

# pytest test_userdetails_api.py -s
