import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
url = reverse('superadmin:vendor_and_user_management:users')


def test_getRequest(api_client, userKids, user):
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert len(resp.data) == 1
    userDetails = resp.data[0]
    assert userDetails['first_name'] == ''
    assert userDetails['last_name'] == ''
    assert userDetails['email'] == 'user@moppetto.com'
    assert userDetails['city'] == user.userdetails.city.name
    assert userDetails['country'] == user.userdetails.city.country.name


def test_postRequest(api_client, city, country):
    data = {
        'password': 'password',
        'first_name': 'firstName',
        'last_name': 'last',
        'email': 'user3@gmail.com',
        'city': city.name,
        'country': country.name
    }

    resp = api_client.post(url, data=data, format='json')

    assert resp.status_code == 201
    all_users = User.objects.all()
    assert len(all_users) == 1
    userDetails = resp.data
    assert userDetails['first_name'] == data['first_name']
    assert userDetails['last_name'] == data['last_name']
    assert userDetails['email'] == data['email']
    assert userDetails['city'] == data['city']
    assert userDetails['country'] == data['country']


def test_patchRequest(api_client, userKids):
    resp = api_client.patch(url)
    assert resp.status_code == 405

    resp = api_client.put(url)
    assert resp.status_code == 405

    resp = api_client.delete(url)
    assert resp.status_code == 405


# pytest test_users_api.py -s
