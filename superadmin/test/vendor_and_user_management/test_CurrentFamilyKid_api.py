import pytest
from django.urls import reverse

url = reverse(
    'superadmin:vendor_and_user_management:CurrentFamilyKid', kwargs={'id': 1})


def test_request(api_client):
    resp = api_client.get(url)
    assert resp.status_code == 401

    resp = api_client.put(url)
    assert resp.status_code == 401

    resp = api_client.post(url)
    assert resp.status_code == 401

    resp = api_client.patch(url)
    assert resp.status_code == 401

    resp = api_client.delete(url)
    assert resp.status_code == 401


def test_getRequest(api_client, user, userKids):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 405


def test_postRequest(api_client, user, userKids):
    api_client.force_authenticate(user)
    resp = api_client.post(url)
    assert resp.status_code == 405


def test_patchRequest(api_client, user, userKids):
    data = {
        'dob': '2021-01-01'
    }
    api_client.force_authenticate(user)

    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == 200
    assert resp.data['dob'] == data['dob']

    data['image'] = {
        "name": 'image',
        "file": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACQAAAAkCAQAAABLCVATAAAA5UlEQVRIx+3Vzw2CMBTH8e8RppAVmEAvbOMCPTGAY/QGC/gncRPtJOZ5sQQDvD7BmGjs79jy4ZU2PPjYKNmypVyG5LTIIy35fKjpGEFo7A9WOOouOwThhsdzQxB2vVlHNcX4p/fH+OTcoBp5GZKxqtzE0v7WhnFDqJ5Yqqf+JejE5R3QnowV16XQngyA9TIoMgVhCTTGzIDGmSQUOJuYBBQoyDkamAS0ASDjkGQMFUVKZwzfKFI6Yzi1SOmM6fgjpTHGexQoEoz5QoYE8yU/NjcLcvZ2pKeyN0gt3tay9Sgt+z/Gxx1bfJWigCzsjQAAAABJRU5ErkJggg=="
    }

    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == 200
    assert resp.data['image'] != None


def test_putRequest(api_client, user, userKids):
    api_client.force_authenticate(user)
    resp = api_client.put(url)
    assert resp.status_code == 405


def test_deleteRequest(api_client, user, userKids):
    api_client.force_authenticate(user)
    resp = api_client.delete(url)
    assert resp.status_code == 200
    
# pytest test_CurrentFamilyKid_api.py -s
