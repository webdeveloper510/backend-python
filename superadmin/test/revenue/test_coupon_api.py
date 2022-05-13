import pytest
from django.urls import reverse

url = reverse('superadmin:revenue:coupon', kwargs={'cid': 1})


def test_getRequest(api_client, coupon, country):
    resp = api_client.get(url)
    assert resp.status_code == 405
    


def test_postRequest(api_client, coupon, country):
    resp = api_client.post(url, data={})
    assert resp.status_code == 405


def test_postRequest(api_client, coupon, country):
    resp = api_client.put(url, data={})
    assert resp.status_code == 405


def test_deleteRequest(api_client, coupon, country):
    resp = api_client.delete(url)
    assert resp.status_code == 204


def test_patchRequest(api_client, coupon, country):
    data = {
        'coupon_code': 'ASDF43',
        'max_number_of_coupon': 100,
        'status': 'ACTIVE'
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == 200
    assert resp.data['coupon_code'] == data['coupon_code']
    assert resp.data['max_number_of_coupon'] == data['max_number_of_coupon']
    assert resp.data['status'] == data['status']

# pytest test_coupon_api.py -s
