import pytest
from django.urls import reverse

url = reverse('superadmin:vendor_and_user_management:userprofile',
              kwargs={'id': 1})


def test_getRequest(api_client, userKids):
    resp = api_client.get(url)
    assert resp.status_code == 200
    print(resp.data)


# pytest test_userprofile_api.test
