import pytest
from django.urls import reverse

url = reverse('superadmin:perticipants:search_activity_perticipents')


def test_getRequestWithParams(api_client, country, vendor, activity, location):
    resp = api_client.get(url)
    assert resp.status_code == 400

    params = '?country=India'
    resp = api_client.get(url+params)
    assert resp.status_code == 400

    params = '?country=India&vendor_code=ER3T'
    resp = api_client.get(url+params)
    assert resp.status_code == 400

    params1 = params+'&activity_title=Swimming for toddlers & beginners'

    resp = api_client.get(url+params1)
    assert resp.status_code == 400

    params = params+'&activity_code=3RTY'
    resp = api_client.get(url+params)
    assert resp.status_code == 400

    params = params+'&location=4'
    resp = api_client.get(url+params)
    assert resp.status_code == 404

    new_params = '?country=USWQ&vendor_code=ER3T&activity_code=3RTY&location=4'
    resp = api_client.get(url+new_params)
    assert resp.status_code == 404

    new_params = '?country=India&vendor_code=1234ER3T&activity_code=3RTY&location=4'
    resp = api_client.get(url+new_params)
    assert resp.status_code == 404

    new_params = '?country=India&vendor_code=1234ER3T&activity_code=adf&location=4'
    resp = api_client.get(url+new_params)
    assert resp.status_code == 404

    new_params = '?country=India&vendor_code=1234ER3T&activity_code=adf&location=' + \
        str(location.id)
    resp = api_client.get(url+new_params)
    assert resp.status_code == 404


def test_searchParticipantOfDayAccess(api_client):
    pass
