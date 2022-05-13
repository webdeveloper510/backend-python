from django.contrib.auth import get_user_model
User = get_user_model()
import pytest
from django.urls import reverse


url = reverse('superadmin:vendor_and_user_management:ChangePassword')

data = {
    'old_password': 'password',
    'new_password': 'password1'
}


def test_userByPostRequestWithoutLogin(api_client, user):
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 401

    resp = api_client.get(url)
    assert resp.status_code == 401

    resp = api_client.put(url)
    assert resp.status_code == 401

    resp = api_client.patch(url)
    assert resp.status_code == 401

    resp = api_client.delete(url)
    assert resp.status_code == 401


def test_userByPostRequest(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400
    data['new_password'] = 'p05drm3ly'
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 200
    change_pass_user = User.objects.get(id=user.id)
    assert change_pass_user.check_password(data['new_password'])
    # assert change_pass_user.check_password('password1')


def test_getRequest(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 405


def test_putRequest(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.put(url)
    assert resp.status_code == 405


def test_patchRequest(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.patch(url)
    assert resp.status_code == 405


def test_deleteRequest(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.delete(url)
    assert resp.status_code == 405

# pytest test_user_api.py -s
