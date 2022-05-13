import pytest
from faker import Faker
from superadmin.subapps.media_and_groupings import models
from superadmin.subapps.media_and_groupings import serializers_categories
from django.urls import reverse
from rest_framework import status

fake = Faker()

url = reverse('superadmin:media_and_groupings:categories')


def test_getRequestWihtoutLogin(api_client, category):
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

    all_category = models.Category.objects.all()
    serializer = serializers_categories.CategorySerializer(all_category, many=True)
    assert resp.data == serializer.data

@pytest.mark.django_db
def test_postRequestWihtoutLogin(api_client):
    name= fake.name()
    data= {
        'name': name, 
        'index': 10, 
        'status': 'ACTIVE', 

    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED

    all_category = models.Category.objects.all()
    assert len(all_category) == 1
    cat = all_category.filter(name=name).first()
    assert cat.index == 1

    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    subCatName = fake.name()
    data['subCategory'] = [
        {
            "name": subCatName,
            "status": "ACTIVE"
        }
    ]
    new_name = fake.name()
    data['name'] = new_name
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    subCat = models.SubCategory.objects.all()
    assert len(subCat) == 1

def test_patchRequestWihtoutLogin(api_client):
    resp = api_client.patch(url)
    assert resp.status_code == 405

def test_deleteRequestWihtoutLogin(api_client):
    resp = api_client.delete(url)
    assert resp.status_code == 405

def test_getRequestByUser(api_client, user, category):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

    all_category = models.Category.objects.all()
    serializer = serializers_categories.CategorySerializer(all_category, many=True)
    assert resp.data == serializer.data

def test_getRequestByVendorUser(api_client, vendorUser, category):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

    all_category = models.Category.objects.all()
    serializer = serializers_categories.CategorySerializer(all_category, many=True)
    assert resp.data == serializer.data

def test_getRequestBySubAdmin(api_client, subAdmin, category):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

    all_category = models.Category.objects.all()
    serializer = serializers_categories.CategorySerializer(all_category, many=True)
    assert resp.data == serializer.data
    

def test_getRequestBySuperAdmin(api_client, superAdmin, category):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK

    all_category = models.Category.objects.all()
    serializer = serializers_categories.CategorySerializer(all_category, many=True)
    assert resp.data == serializer.data

def test_postRequestByUser(api_client, user):
    api_client.force_authenticate(user)
    name= fake.name()
    data= {
        'name': name, 
        'index': 10, 
        'status': 'ACTIVE', 

    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED

    all_category = models.Category.objects.all()
    assert len(all_category) == 1
    cat = all_category.filter(name=name).first()
    assert cat.index == 1

    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    subCatName = fake.name()
    data['subCategory'] = [
        {
            "name": subCatName,
            "status": "ACTIVE"
        }
    ]
    new_name = fake.name()
    data['name'] = new_name
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    subCat = models.SubCategory.objects.all()
    assert len(subCat) == 1
    

def test_postRequestByVendorUser(api_client, vendorUser):
    api_client.force_authenticate(vendorUser)
    name= fake.name()
    data= {
        'name': name, 
        'index': 10, 
        'status': 'ACTIVE', 

    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED

    all_category = models.Category.objects.all()
    assert len(all_category) == 1
    cat = all_category.filter(name=name).first()
    assert cat.index == 1

    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    subCatName = fake.name()
    data['subCategory'] = [
        {
            "name": subCatName,
            "status": "ACTIVE"
        }
    ]
    new_name = fake.name()
    data['name'] = new_name
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    subCat = models.SubCategory.objects.all()
    assert len(subCat) == 1

def test_postRequestBySubAdmin(api_client, subAdmin):
    api_client.force_authenticate(subAdmin)
    name= fake.name()
    data= {
        'name': name, 
        'index': 10, 
        'status': 'ACTIVE', 

    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED

    all_category = models.Category.objects.all()
    assert len(all_category) == 1
    cat = all_category.filter(name=name).first()
    assert cat.index == 1

    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    subCatName = fake.name()
    data['subCategory'] = [
        {
            "name": subCatName,
            "status": "ACTIVE"
        }
    ]
    new_name = fake.name()
    data['name'] = new_name
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    subCat = models.SubCategory.objects.all()
    assert len(subCat) == 1

def test_postRequestBySuperAdmin(api_client, superAdmin):
    api_client.force_authenticate(superAdmin)
    name= fake.name()
    data= {
        'name': name,
        'index': 10, 
        'status': 'ACTIVE', 

    }
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED

    all_category = models.Category.objects.all()
    assert len(all_category) == 1
    cat = all_category.filter(name=name).first()
    assert cat.index == 1

    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    subCatName = fake.name()
    data['subCategory'] = [
        {
            "name": subCatName,
            "status": "ACTIVE"
        }
    ]
    new_name = fake.name()
    data['name'] = new_name
    resp = api_client.post(url, data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    subCat = models.SubCategory.objects.all()
    assert len(subCat) == 1


def test_patchRequestByUser(api_client, user, category):
    api_client.force_authenticate(user)
    data= {}
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == 405


def test_patchRequestByVendorUser(api_client, vendorUser, category):
    api_client.force_authenticate(vendorUser)
    data= {}
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == 405

def test_patchRequestBySubAdmin(api_client, subAdmin, category):
    api_client.force_authenticate(subAdmin)
    data= {"name": 'new Cat'}
    url1 = url + '?name='+ category.name
    resp = api_client.patch(url1, data, format='json')
    # assert resp.status_code == status.HTTP_200_OK
    subCat = models.SubCategory.objects.all()
    assert len(subCat) == 0
    subCats = models.SubCategory(
        name="sub cat",
        category=category
    )
    subCats.save()
    data['subCategory'] = [
        {
            "id": subCats.id,
            "name": "SubCate3",
        }
    ]
    url1 = url + '?name=new Cat'
    resp = api_client.patch(url1, data, format='json')
    assert resp.status_code == 405
    

def test_patchRequestBySuperAdmin(api_client, superAdmin, category):
    api_client.force_authenticate(superAdmin)
    data= {"name": 'new Cat'}
    url1 = url + '?name='+ category.name
    resp = api_client.patch(url1, data, format='json')
    # assert resp.status_code == status.HTTP_200_OK
    subCat = models.SubCategory.objects.all()
    assert len(subCat) == 0
    subCats = models.SubCategory(
        name="sub cat",
        category=category
    )
    subCats.save()
    data['subCategory'] = [
        {
            "id": subCats.id,
            "name": "SubCate3",
        }
    ]
    url1 = url + '?name=new Cat'
    resp = api_client.patch(url1, data, format='json')
    assert resp.status_code == 405



def test_deleteRequestByUser(api_client, user, category, bannerDetails):
    api_client.force_authenticate(user)
    url1 = url + '?name='+ category.name
    resp = api_client.delete(url1)
    assert resp.status_code == 405

def test_deleteRequestBySubAdmin(api_client, subAdmin, category, bannerDetails):
    api_client.force_authenticate(subAdmin)
    url1 = url + '?name='+ category.name
    resp = api_client.delete(url1)
    assert resp.status_code == 405

def test_deleteRequestBySubAdminVendor(api_client, vendorUser, category, bannerDetails):
    api_client.force_authenticate(vendorUser)
    url1 = url + '?name='+ category.name
    resp = api_client.delete(url1)
    assert resp.status_code == 405


def test_deleteRequestBySuperAdmin(api_client, superAdmin, category, bannerDetails):
    api_client.force_authenticate(superAdmin)
    name = category.name
    new_cat = category
    new_cat.id =None
    new_cat.name = 'Cat3'
    new_cat.save()

    url1 = url + '?name='+ new_cat.name
    resp = api_client.delete(url1)
    assert resp.status_code == 405
