import pytest
from django.urls import reverse
from faker import Faker
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_attributes as serializers


fake = Faker()
name = fake.name()


url = reverse('superadmin:media_and_groupings:attributes')
data = {
    'name' : name
}


def test_requestWithoutLogin(api_client, attribute):
    resp = api_client.get(url)
    assert resp.status_code == 200
    all = models.Attribute.objects.all()

    assert len(all) == 1
    
    serializer = serializers.AttributeSerializer(all, many=True)
    assert resp.data == serializer.data

    resp = api_client.patch(url)
    assert resp.status_code == 405

    resp = api_client.put(url)
    assert resp.status_code == 405

    resp = api_client.delete(url)
    assert resp.status_code == 405


@pytest.mark.django_db
def test_postRequestWithoutLogin(api_client):
    resp = api_client.post(url, data)
    assert resp.status_code == 201
    all_attr  = models.Attribute.objects.all() 
    assert len(all_attr) == 1
    assert all_attr[0].index == 1
    serializer = serializers.AttributeSerializer(all_attr[0])
    assert resp.data == serializer.data


    resp = api_client.post(url, data)
    assert resp.status_code == 400

    data['name'] = fake.name()
    data['subAttribute'] = [
        {"name": "Subatt1", "status": "ACTIVE"},
        {"name": "Subatt2", "status": "ACTIVE"}
    ]
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 201
    sub_att = models.SubAttribute.objects.all()
    all_attr = models.Attribute.objects.all()

    assert len(sub_att) == 2
    assert len(all_attr) == 2
    assert sub_att[0].name == "Subatt1"



def test_requestByUser(api_client, user, attribute):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all = models.Attribute.objects.all()

    assert len(all) == 1
    
    serializer = serializers.AttributeSerializer(all, many=True)
    assert resp.data == serializer.data


def test_requestByVendorUser(api_client, vendorUser, attribute):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all = models.Attribute.objects.all()

    assert len(all) == 1

    serializer = serializers.AttributeSerializer(all, many=True)
    assert resp.data == serializer.data


def test_requestBySubAdmin(api_client, subAdmin, attribute):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all = models.Attribute.objects.all()

    assert len(all) == 1

    serializer = serializers.AttributeSerializer(all, many=True)
    assert resp.data == serializer.data


def test_requestBySuperAdmin(api_client, superAdmin, attribute):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == 200
    all = models.Attribute.objects.all()

    assert len(all) == 1

    serializer = serializers.AttributeSerializer(all, many=True)
    assert resp.data == serializer.data


# POST request test cases
def test_postRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.post(url, data)
    assert resp.status_code == 201
    all_attr  = models.Attribute.objects.all() 
    assert len(all_attr) == 1
    assert all_attr[0].index == 1
    serializer = serializers.AttributeSerializer(all_attr[0])
    assert resp.data == serializer.data


    resp = api_client.post(url, data)
    assert resp.status_code == 400

    data['name'] = fake.name()
    data['subAttribute'] = [
        {"name": "Subatt1", "status": "ACTIVE"},
        {"name": "Subatt2", "status": "ACTIVE"}
    ]
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 201
    sub_att = models.SubAttribute.objects.all()
    all_attr = models.Attribute.objects.all()

    assert len(sub_att) == 2
    assert len(all_attr) == 2
    assert sub_att[0].name == "Subatt1"


def test_postRequestByVendorUser(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.post(url, data)
    assert resp.status_code == 201
    all_attr  = models.Attribute.objects.all() 
    assert len(all_attr) == 1
    # assert all_attr[0].name == name
    assert all_attr[0].index == 1
    serializer = serializers.AttributeSerializer(all_attr[0])
    assert resp.data == serializer.data


    resp = api_client.post(url, data)
    assert resp.status_code == 400

    data['name'] = fake.name()
    data['subAttribute'] = [
        {"name": "Subatt1", "status": "ACTIVE"},
        {"name": "Subatt2", "status": "ACTIVE"}
    ]
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 201
    sub_att = models.SubAttribute.objects.all()
    all_attr = models.Attribute.objects.all()

    assert len(sub_att) == 2
    assert len(all_attr) == 2
    assert sub_att[0].name == "Subatt1"

    data['name'] = name


def test_postRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    resp = api_client.post(url, data)
    assert resp.status_code == 201
    all_attr  = models.Attribute.objects.all() 
    assert len(all_attr) == 1
    # assert all_attr[0].name == name
    assert all_attr[0].index == 1
    serializer = serializers.AttributeSerializer(all_attr[0])
    assert resp.data == serializer.data


    resp = api_client.post(url, data)
    assert resp.status_code == 400

    data['name'] = fake.name()
    data['subAttribute'] = [
        {"name": "Subatt1", "status": "ACTIVE"},
        {"name": "Subatt2", "status": "ACTIVE"}
    ]
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 201
    sub_att = models.SubAttribute.objects.all()
    all_attr = models.Attribute.objects.all()

    assert len(sub_att) == 2
    assert len(all_attr) == 2
    assert sub_att[0].name == "Subatt1"
    data['name'] = name


def test_postRequestBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.post(url, data)
    assert resp.status_code == 201
    all_attr  = models.Attribute.objects.all() 
    assert len(all_attr) == 1
    # assert all_attr[0].name == name
    assert all_attr[0].index == 1
    serializer = serializers.AttributeSerializer(all_attr[0])
    assert resp.data == serializer.data


    resp = api_client.post(url, data)
    assert resp.status_code == 400

    data['name'] = fake.name()
    data['subAttribute'] = [
        {"name": "Subatt1", "status": "ACTIVE"},
        {"name": "Subatt2", "status": "ACTIVE"}
    ]
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == 201
    sub_att = models.SubAttribute.objects.all()
    all_attr = models.Attribute.objects.all()

    assert len(sub_att) == 2
    assert len(all_attr) == 2
    assert sub_att[0].name == "Subatt1"
    data['name'] = name

# POST REQUESTS TEST CASES COMPLETE

# PUT METHOD TEST CASES COMPLETE

def test_putRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    resp = api_client.put(url)
    assert resp.status_code == 405

def test_putRequestByVendorUser(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.put(url)
    assert resp.status_code == 405

def test_putRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    resp = api_client.put(url)
    assert resp.status_code == 405

def test_putRequestBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.put(url)
    assert resp.status_code == 405

# PUT METHOD TEST CASES COMPLETE

def test_patchByUser(api_client, user, attribute):
    api_client.force_authenticate(user)
    new_name = fake.name()
    data = {}
    data['name'] = new_name
    url1 = url + '?name=' + attribute.name
    resp = api_client.patch(url1, data, format='json')
    assert resp.status_code == 405

def test_patchByVendorUser(api_client, vendorUser, attribute):
    api_client.force_authenticate(vendorUser)
    new_name = fake.name()
    data = {}
    data['name'] = new_name
    url1 = url + '?name=' + attribute.name
    resp = api_client.patch(url1, data, format='json')
    assert resp.status_code == 405

def test_patchBysubAdmin(api_client, subAdmin, attribute):
    api_client.force_authenticate(subAdmin)
    new_name = fake.name()
    data = {}
    data['name'] = new_name
    url1 = url + '?name=' + attribute.name
    resp = api_client.patch(url1, data, format='json')
    assert resp.status_code == 405


def test_patchBysuperAdmin(api_client, superAdmin, attribute):
    api_client.force_authenticate(superAdmin)
    new_name = fake.name()
    data = {}
    data['name'] = new_name
    url1 = url + '?name=' + attribute.name
    resp = api_client.patch(url1, data, format='json')
    assert resp.status_code == 405

# PATCH REQUEST COMPLETE

# DELETE REQUEST 

def test_deleteByUser(api_client, user, attribute):
    url1 = url + "?name=" + attribute.name
    api_client.force_authenticate(user)
    resp = api_client.delete(url1)
    assert resp.status_code == 405

def test_deleteByVendorUser(api_client, vendorUser, attribute):
    url1 = url + "?name=" + attribute.name
    api_client.force_authenticate(vendorUser)
    resp = api_client.delete(url1)
    assert resp.status_code == 405

def test_deleteBySubAdmin(api_client, subAdmin, attribute):
    url1 = url + "?name=" + attribute.name
    api_client.force_authenticate(subAdmin)
    resp = api_client.delete(url1)
    assert resp.status_code == 405

def test_deleteBySuperAdmin(api_client, superAdmin, attribute):
    url1 = url + "?name=" + attribute.name
    api_client.force_authenticate(superAdmin)
    resp = api_client.delete(url1)
    assert resp.status_code == 405