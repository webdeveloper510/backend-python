import pytest
from django.urls import reverse
from superadmin.subapps.revenue.models import Coupons


url = reverse('superadmin:revenue:coupons')


def test_getRequest(api_client, coupon, country):
    resp = api_client.get(url)
    assert resp.status_code == 200
    data = resp.data[0]
    used_coupon = coupon.coupondetails.all().count()
    assert data['country'] == country.name
    assert data['coupon_code'] == coupon.coupon_code
    assert data['count_of_used_coupon'] == used_coupon
    assert data['discountType'] == coupon.discountType
    assert int(float(data['discount_value'])) == int(
        float(coupon.discount_value))
    assert data['from_date'] == coupon.from_date
    assert data['to_date'] == coupon.to_date
    assert data['first_name'] == None
    assert data['last_name'] == None
    assert data['max_number_of_coupon'] == coupon.max_number_of_coupon
    assert data['status'] == coupon.status
    assert data['discount_apply_type'] == 'ADVANCE PREMIUM ENTERPRISE'


def test_postRequest(api_client, country, subscriptionPackages):
    data = {
        "coupon_code": "ASDF44l",
        "discount_value": 5,
        "country": country.name,
        "from_date": "2021-09-01",
        "to_date": "2021-10-01",
        "max_number_of_coupon": "2",
        "subscription": ["ADVANCE", "PREMIUM"]
    }
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    assert resp.data['discountType'] == 'value'
    Coupons.objects.get(id=resp.data['id']).delete()
    data['discountType'] = 'percent'
    del data['country']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400
    data['country'] = country.name
    del data['max_number_of_coupon']
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400
    data['max_number_of_coupon'] = 10

    resp = api_client.post(url, data=data, format='json')
    print(resp.data)
    assert resp.status_code == 201
    res_data = resp.data
    assert res_data['country'] == country.name
    assert res_data['coupon_code'] == data["coupon_code"]
    assert res_data['count_of_used_coupon'] == 0
    assert res_data['discountType'] == data['discountType']
    assert int(float(res_data['discount_value'])) == int(
        float('5'))
    assert res_data['from_date'] == data["from_date"]
    assert res_data['to_date'] == data['to_date']
    assert res_data['first_name'] == None
    assert res_data['last_name'] == None
    assert res_data['max_number_of_coupon'] == data['max_number_of_coupon']
    assert res_data['status'] == 'SCHEDULED'
    assert res_data['discount_apply_type'] == 'ADVANCE PREMIUM'


def test_patchRequest(api_client, country, subscriptionPackages):
    resp = api_client.patch(url, data={})
    assert resp.status_code == 405


def test_putRequest(api_client, country, subscriptionPackages):
    resp = api_client.put(url, data={})
    assert resp.status_code == 405


def test_deleteRequest(api_client, country, subscriptionPackages):
    resp = api_client.delete(url, data={})
    assert resp.status_code == 405
# pytest test_coupons_api.py -s
