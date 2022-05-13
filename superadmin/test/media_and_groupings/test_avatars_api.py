import pytest
from django.urls import reverse
from faker import Faker
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_avatars as serializers


data = {
    'name' : "Api avatar",
    'type' : 'GIRL',
    "media": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACQAAAAkCAQAAABLCVATAAAA5UlEQVRIx+3Vzw2CMBTH8e8RppAVmEAvbOMCPTGAY/QGC/gncRPtJOZ5sQQDvD7BmGjs79jy4ZU2PPjYKNmypVyG5LTIIy35fKjpGEFo7A9WOOouOwThhsdzQxB2vVlHNcX4p/fH+OTcoBp5GZKxqtzE0v7WhnFDqJ5Yqqf+JejE5R3QnowV16XQngyA9TIoMgVhCTTGzIDGmSQUOJuYBBQoyDkamAS0ASDjkGQMFUVKZwzfKFI6Yzi1SOmM6fgjpTHGexQoEoz5QoYE8yU/NjcLcvZ2pKeyN0gt3tay9Sgt+z/Gxx1bfJWigCzsjQAAAABJRU5ErkJggg=="
}
#  pytest test_avatarModels.py -s 
url = reverse('superadmin:media_and_groupings:avatars')

def test_getRequest(api_client, avatars):
    resp = api_client.get(url)
    all_avatars = models.Avatar.objects.all()
    serializer = serializers.AvatarSerializer(all_avatars, many=True)
    assert resp.status_code == 200
    assert resp.data == serializer.data


def test_getByUserRequest(api_client, user, avatars):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    all_avatars = models.Avatar.objects.all()
    serializer = serializers.AvatarSerializer(all_avatars, many=True)
    assert resp.status_code == 200
    assert resp.data == serializer.data


def test_getRequestByVendor(api_client, vendorUser, avatars):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    all_avatars = models.Avatar.objects.all()
    serializer = serializers.AvatarSerializer(all_avatars, many=True)
    assert resp.status_code == 200
    assert resp.data == serializer.data

def test_getRequestbySuperAdmin(api_client, superAdmin, avatars):

    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    all_avatars = models.Avatar.objects.all()
    serializer = serializers.AvatarSerializer(all_avatars, many=True)
    assert resp.status_code == 200
    assert resp.data == serializer.data

@pytest.mark.django_db
def test_postRequest(api_client):
    resp = api_client.post(url, data=data)
    assert resp.status_code == 200
    all_avatars = models.Avatar.objects.all()
    assert len(all_avatars) == 1
    assert all_avatars[0].status == 'ACTIVE'

    

@pytest.mark.django_db
def test_postRequestBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.post(url, data=data)
    assert resp.status_code == 200
    all_avatars = models.Avatar.objects.all()
    assert len(all_avatars) == 1
    assert all_avatars[0].status == 'ACTIVE'


@pytest.mark.django_db
def test_postRequestByVendor(api_client, vendor):
    api_client.force_authenticate(vendor)
    resp = api_client.post(url, data=data)
    assert resp.status_code == 200
    all_avatars = models.Avatar.objects.all()
    assert len(all_avatars) == 1
    assert all_avatars[0].status == 'ACTIVE'


@pytest.mark.django_db
def test_postRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.post(url, data=data)
    assert resp.status_code == 200
    all_avatars = models.Avatar.objects.all()
    assert len(all_avatars) == 1
    assert all_avatars[0].status == 'ACTIVE'


@pytest.mark.django_db
def test_patchRequest(api_client, db):
    resp = api_client.patch(url, data=data)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_patchRequestByUser(api_client, user,db):
    api_client.force_authenticate(user)
    resp = api_client.patch(url, data=data)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_patchRequestByVendor(api_client, vendor, db):
    api_client.force_authenticate(vendor)
    resp = api_client.patch(url, data=data)
    assert resp.status_code == 405

@pytest.mark.django_db
def test_patchRequestBySuperAdmin(api_client, superAdmin, db):
    api_client.force_authenticate(superAdmin)
    resp = api_client.patch(url, data=data)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_putRequest(api_client, db):
    resp = api_client.put(url, data=data)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_putRequestByUser(api_client, user,db):
    api_client.force_authenticate(user)
    resp = api_client.put(url, data=data)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_putRequestByVendor(api_client, vendor, db):
    api_client.force_authenticate(vendor)
    resp = api_client.put(url, data=data)
    assert resp.status_code == 405

@pytest.mark.django_db
def test_putRequestBySuperAdmin(api_client, superAdmin, db):
    api_client.force_authenticate(superAdmin)
    resp = api_client.put(url, data=data)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_deleteRequest(api_client, db):
    resp = api_client.delete(url, data=data)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_deleteRequestByUser(api_client, user,db):
    api_client.force_authenticate(user)
    resp = api_client.delete(url, data=data)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_deleteRequestByVendor(api_client, vendor, db):
    api_client.force_authenticate(vendor)
    resp = api_client.delete(url, data=data)
    assert resp.status_code == 405

@pytest.mark.django_db
def test_deleteRequestBySuperAdmin(api_client, superAdmin, db):
    api_client.force_authenticate(superAdmin)
    resp = api_client.delete(url, data=data)
    assert resp.status_code == 405


# pytest test_avatars_api.py -s


