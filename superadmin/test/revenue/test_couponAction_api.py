import pytest
import datetime
from django.urls import reverse


url = reverse('superadmin:revenue:couponAction',
              kwargs={'cid': 1, 'action': 'ACTIVE'})


def test_getRequest(api_client, coupon, country):
    print(coupon.status)
    resp = api_client.get(url)
    assert resp.status_code == 400


def test_chageValue(api_client, coupon, country):
    today = datetime.datetime.now()
    fiveDaysAgo = today - datetime.timedelta(days=5)
    thirtyDaysafter = today + datetime.timedelta(days=30)
    coupon.from_date = fiveDaysAgo
    coupon.to_date = thirtyDaysafter
    coupon.status = 'ACTIVE'
    coupon.save()

    url1 = reverse('superadmin:revenue:couponAction',
                   kwargs={'cid': 1, 'action': 'SUSPENDED'})

    resp = api_client.get(url1)

    assert resp.status_code == 200


def test_whenActiveStatus(api_client, coupon, country):
    today = datetime.datetime.now()
    fiveDaysAgo = today - datetime.timedelta(days=5)
    thirtyDaysafter = today + datetime.timedelta(days=30)
    coupon.from_date = fiveDaysAgo
    coupon.to_date = thirtyDaysafter
    coupon.status = 'ACTIVE'
    coupon.save()

    url1 = reverse('superadmin:revenue:couponAction',
                   kwargs={'cid': 1, 'action': 'SCHEDULED'})

    resp = api_client.get(url1)
    assert resp.status_code == 400

    url1 = reverse('superadmin:revenue:couponAction',
                   kwargs={'cid': 1, 'action': 'EXPIRED'})
    resp = api_client.get(url1)
    assert resp.status_code == 400


def test_statusExpired(api_client, coupon, country):
    today = datetime.datetime.now()
    fiveDaysAgo = today - datetime.timedelta(days=5)
    thirtyDaysafter = today - datetime.timedelta(days=30)
    coupon.from_date = thirtyDaysafter
    coupon.to_date = fiveDaysAgo
    coupon.status = 'EXPIRED'
    coupon.save()

    url1 = reverse('superadmin:revenue:couponAction',
                   kwargs={'cid': 1, 'action': 'SCHEDULED'})

    resp = api_client.get(url1)
    assert resp.status_code == 400


def test_statusSUSPENDED(api_client, coupon, country):
    today = datetime.datetime.now()
    fiveDaysAgo = today - datetime.timedelta(days=5)
    thirtyDaysafter = today - datetime.timedelta(days=30)
    coupon.from_date = thirtyDaysafter
    coupon.to_date = fiveDaysAgo
    coupon.status = 'SUSPENDED'
    coupon.save()

    url1 = reverse('superadmin:revenue:couponAction',
                   kwargs={'cid': 1, 'action': 'SCHEDULED'})

    resp = api_client.get(url1)
    assert resp.status_code == 400
    to_date = today + datetime.timedelta(days=5)
    coupon.to_date = to_date
    coupon.save()
    url1 = reverse('superadmin:revenue:couponAction',
                   kwargs={'cid': 1, 'action': 'SCHEDULED'})
    resp = api_client.get(url1)
    assert resp.status_code == 400

    url1 = reverse('superadmin:revenue:couponAction',
                   kwargs={'cid': 1, 'action': 'ACTIVE'})
    resp = api_client.get(url1)
    assert resp.status_code == 200

    from_date = today + datetime.timedelta(days=5)
    to_date = today + datetime.timedelta(days=365)
    coupon.from_date = from_date
    coupon.to_date = to_date
    coupon.save()
    url1 = reverse('superadmin:revenue:couponAction',
                   kwargs={'cid': 1, 'action': 'ACTIVE'})
    resp = api_client.get(url1)
    assert resp.status_code == 400

    url1 = reverse('superadmin:revenue:couponAction',
                   kwargs={'cid': 1, 'action': 'SCHEDULED'})
    resp = api_client.get(url1)
    assert resp.status_code == 200

# pytest test_couponAction_api.py -s
