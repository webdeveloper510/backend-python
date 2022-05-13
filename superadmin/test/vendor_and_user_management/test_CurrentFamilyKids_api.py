import pytest
from django.urls import reverse


url = reverse('superadmin:vendor_and_user_management:CurrentFamilyKids')
data = {
    'first_name': 'kids1',
    'last_name': 'lastname',
    'dob': '2021-07-09',
    'image': {
        "name": 'image',
        "file": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACQAAAAkCAQAAABLCVATAAAA5UlEQVRIx+3Vzw2CMBTH8e8RppAVmEAvbOMCPTGAY/QGC/gncRPtJOZ5sQQDvD7BmGjs79jy4ZU2PPjYKNmypVyG5LTIIy35fKjpGEFo7A9WOOouOwThhsdzQxB2vVlHNcX4p/fH+OTcoBp5GZKxqtzE0v7WhnFDqJ5Yqqf+JejE5R3QnowV16XQngyA9TIoMgVhCTTGzIDGmSQUOJuYBBQoyDkamAS0ASDjkGQMFUVKZwzfKFI6Yzi1SOmM6fgjpTHGexQoEoz5QoYE8yU/NjcLcvZ2pKeyN0gt3tay9Sgt+z/Gxx1bfJWigCzsjQAAAABJRU5ErkJggg=="
    }
}


def test_requestWithoutLogin(api_client):
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


def test_addKidds(api_client, user):
    api_client.force_authenticate(user)

    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 400


def test_addKidsWithFamily(api_client, userFamily):
    api_client.force_authenticate(userFamily)
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    assert resp.data['first_name'] == data['first_name']
    assert resp.data['last_name'] == data['last_name']

    family_url = reverse(
        'superadmin:vendor_and_user_management:currentuserfamily')
    resp = api_client.get(family_url)
    assert resp.status_code == 200
    assert len(resp.data['kids']) == 1
    kids_dict = dict(resp.data['kids'][0])

    assert kids_dict['first_name'] == data['first_name']
    assert kids_dict['last_name'] == data['last_name']


def test_addKidsWithFamilyWithAvatar(api_client, userFamily, avatar):
    api_client.force_authenticate(userFamily)
    del data['image']
    data['avatar'] = avatar.id
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == 201
    assert resp.data['image'] != None


def test_requestWithoutLogin(api_client, userFamily):
    api_client.force_authenticate(userFamily)

    resp = api_client.get(url)
    assert resp.status_code == 405

    resp = api_client.put(url)
    assert resp.status_code == 405

    resp = api_client.patch(url)
    assert resp.status_code == 405

    resp = api_client.delete(url)
    assert resp.status_code == 405
# pytest test_CurrentFamilyKids_api.py -s
