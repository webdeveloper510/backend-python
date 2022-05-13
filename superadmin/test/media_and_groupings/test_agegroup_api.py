import pytest
from faker import Faker
from django.urls import reverse
from rest_framework import status
from superadmin.subapps.media_and_groupings import serializers_age_groups as serializers
from superadmin.subapps.media_and_groupings import models as m_models

fake = Faker()
url = reverse('superadmin:media_and_groupings:agegroup', kwargs={'id': 1})


def test_getRequestWithoutLogin(api_client, ageGroup):
    data = {
        "name": "Baby Groups1"
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == "Baby Groups1"


def test_postRequestWithoutLogin(api_client):
    resp = api_client.post(url)
    assert resp.status_code == 405


def test_patchRequestWithoutLogin(api_client, ageGroup):
    data = {
        "name": "Baby Groups1"
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == "Baby Groups1"


def test_putRequestWithoutLogin(api_client, ageGroup, country):
    text = fake.text()
    new_name = fake.name()
    data = {
        "name": new_name,
        "description": text,
        "min_age": 1,
        "max_age": 5,
        "status": 'ACTIVE',
        "country": country.name
    }
    resp = api_client.put(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == new_name
    assert first_group.description == text
    assert first_group.status == 'ACTIVE'

    # try to make new group which is already use

    new_gorup = ageGroup
    new_gorup.id = None
    new_gorup.min_age = 8
    new_gorup.max_age = 10
    new_gorup.save()

    url1 = reverse('superadmin:media_and_groupings:agegroup',
                   kwargs={'id': new_gorup.id})
    data = {
        'name': new_gorup.name,
        "min_age": 1,
        "max_age": 5,
        'description': new_gorup.description
    }
    resp = api_client.put(url1, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    new_g = m_models.AgeGroup.objects.get(id=new_gorup.id)
    assert new_g.min_age == 8
    assert new_g.max_age == 10

    data["min_age"] = 1
    data["max_age"] = 8

    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    old_first_group = m_models.AgeGroup.objects.get(id=first_group.id)
    assert old_first_group.min_age == 1
    assert old_first_group.max_age == 5


def test_deleteRequestWithoutLogin(api_client, ageGroup):
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    age_group = m_models.AgeGroup.objects.get(id=1)
    serializer = serializers.AgeGroupSerializer(age_group)
    assert resp.data == serializer.data


def test_getRequestByUser(api_client, user, ageGroup):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    age_group = m_models.AgeGroup.objects.get(id=1)
    serializer = serializers.AgeGroupSerializer(age_group)
    assert resp.data == serializer.data


def test_getRequestByVendorUser(api_client, vendorUser, ageGroup):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    age_group = m_models.AgeGroup.objects.get(id=1)
    serializer = serializers.AgeGroupSerializer(age_group)
    assert resp.data == serializer.data


def test_getRequestBySubAdmin(api_client, subAdmin, ageGroup):
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    age_group = m_models.AgeGroup.objects.get(id=1)
    serializer = serializers.AgeGroupSerializer(age_group)
    assert resp.data == serializer.data


def test_getRequestBySuperAdmin(api_client, superAdmin, ageGroup):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    age_group = m_models.AgeGroup.objects.get(id=1)
    serializer = serializers.AgeGroupSerializer(age_group)
    assert resp.data == serializer.data


def test_postRequestByUser(api_client, user, ageGroup):
    api_client.force_authenticate(user)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_postRequestByVendorUser(api_client, vendorUser, ageGroup):
    api_client.force_authenticate(vendorUser)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_postRequestBySubAdmin(api_client, subAdmin, ageGroup):
    api_client.force_authenticate(subAdmin)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_postRequestBySuperAdmin(api_client, superAdmin, ageGroup):
    api_client.force_authenticate(superAdmin)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patchRequestByUser(api_client, user, ageGroup):
    api_client.force_authenticate(user)
    data = {
        "name": "Baby Groups1"
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == "Baby Groups1"


def test_patchRequestByVendorUser(api_client, vendorUser, ageGroup):
    api_client.force_authenticate(vendorUser)
    data = {
        "name": "Baby Groups1"
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == "Baby Groups1"


def test_patchRequestBySubAdmin(api_client, subAdmin, ageGroup):
    api_client.force_authenticate(subAdmin)
    data = {
        "name": "Baby Groups1"
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == "Baby Groups1"


def test_patchRequestBySuperAdmin(api_client, superAdmin, ageGroup):
    api_client.force_authenticate(superAdmin)
    data = {
        "name": "Baby Groups1"
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == "Baby Groups1"


def test_patchRequestByUser(api_client, user, ageGroup, country):
    api_client.force_authenticate(user)
    text = fake.text()
    new_name = fake.name()
    data = {
        "name": new_name,
        "description": text,
        "min_age": 1,
        "max_age": 5,
        "status": 'ACTIVE',
        "country": country.name
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == new_name
    assert first_group.description == text
    assert first_group.status == 'ACTIVE'

    # try to make new group which is already use

    new_gorup = ageGroup
    new_gorup.id = None
    new_gorup.min_age = 8
    new_gorup.max_age = 10
    new_gorup.save()

    url1 = reverse('superadmin:media_and_groupings:agegroup',
                   kwargs={'id': new_gorup.id})
    data = {
        "min_age": 1,
        "max_age": 5,
    }
    resp = api_client.patch(url1, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    new_g = m_models.AgeGroup.objects.get(id=new_gorup.id)
    assert new_g.min_age == 8
    assert new_g.max_age == 10

    data = {
        "min_age": 1,
        "max_age": 8
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    old_first_group = m_models.AgeGroup.objects.get(id=first_group.id)
    assert old_first_group.min_age == 1
    assert old_first_group.max_age == 5


def test_patchRequestByVendorUser(api_client, vendorUser, ageGroup, country):
    api_client.force_authenticate(vendorUser)
    text = fake.text()
    new_name = fake.name()
    data = {
        "name": new_name,
        "description": text,
        "min_age": 1,
        "max_age": 5,
        "status": 'ACTIVE',
        "country": country.name
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == new_name
    assert first_group.description == text
    assert first_group.status == 'ACTIVE'

    # try to make new group which is already use

    new_gorup = ageGroup
    new_gorup.id = None
    new_gorup.min_age = 8
    new_gorup.max_age = 10
    new_gorup.save()

    url1 = reverse('superadmin:media_and_groupings:agegroup',
                   kwargs={'id': new_gorup.id})
    data = {
        "min_age": 1,
        "max_age": 5,
    }
    resp = api_client.patch(url1, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    new_g = m_models.AgeGroup.objects.get(id=new_gorup.id)
    assert new_g.min_age == 8
    assert new_g.max_age == 10

    data = {
        "min_age": 1,
        "max_age": 8
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    old_first_group = m_models.AgeGroup.objects.get(id=first_group.id)
    assert old_first_group.min_age == 1
    assert old_first_group.max_age == 5


def test_patchRequestBySubAdmin(api_client, subAdmin, ageGroup, country):
    api_client.force_authenticate(subAdmin)
    text = fake.text()
    new_name = fake.name()
    data = {
        "name": new_name,
        "description": text,
        "min_age": 1,
        "max_age": 5,
        "status": 'ACTIVE',
        "country": country.name
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == new_name
    assert first_group.description == text
    assert first_group.status == 'ACTIVE'

    # try to make new group which is already use

    new_gorup = ageGroup
    new_gorup.id = None
    new_gorup.min_age = 8
    new_gorup.max_age = 10
    new_gorup.save()

    url1 = reverse('superadmin:media_and_groupings:agegroup',
                   kwargs={'id': new_gorup.id})
    data = {
        "min_age": 1,
        "max_age": 5,
    }
    resp = api_client.patch(url1, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    new_g = m_models.AgeGroup.objects.get(id=new_gorup.id)
    assert new_g.min_age == 8
    assert new_g.max_age == 10

    data = {
        "min_age": 1,
        "max_age": 8
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    old_first_group = m_models.AgeGroup.objects.get(id=first_group.id)
    assert old_first_group.min_age == 1
    assert old_first_group.max_age == 5


def test_patchRequestBySuperAdmin(api_client, superAdmin, ageGroup, country):
    api_client.force_authenticate(superAdmin)
    text = fake.text()
    new_name = fake.name()
    data = {
        "name": new_name,
        "description": text,
        "min_age": 1,
        "max_age": 5,
        "status": 'ACTIVE',
        "country": country.name
    }
    resp = api_client.patch(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == new_name
    assert first_group.description == text
    assert first_group.status == 'ACTIVE'

    # try to make new group which is already use

    new_gorup = ageGroup
    new_gorup.id = None
    new_gorup.min_age = 8
    new_gorup.max_age = 10
    new_gorup.save()

    url1 = reverse('superadmin:media_and_groupings:agegroup',
                   kwargs={'id': new_gorup.id})
    data = {
        "min_age": 1,
        "max_age": 5,
    }
    resp = api_client.patch(url1, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    new_g = m_models.AgeGroup.objects.get(id=new_gorup.id)
    assert new_g.min_age == 8
    assert new_g.max_age == 10

    data = {
        "min_age": 1,
        "max_age": 8
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    old_first_group = m_models.AgeGroup.objects.get(id=first_group.id)
    assert old_first_group.min_age == 1
    assert old_first_group.max_age == 5


def test_putRequestByUser(api_client, user, ageGroup, country):
    api_client.force_authenticate(user)
    text = fake.text()
    new_name = fake.name()
    data = {
        "name": new_name,
        "description": text,
        "min_age": 1,
        "max_age": 5,
        "status": 'ACTIVE',
        "country": country.name
    }
    resp = api_client.put(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == new_name
    assert first_group.description == text
    assert first_group.status == 'ACTIVE'

    # try to make new group which is already use

    new_gorup = ageGroup
    new_gorup.id = None
    new_gorup.min_age = 8
    new_gorup.max_age = 10
    new_gorup.save()

    url1 = reverse('superadmin:media_and_groupings:agegroup',
                   kwargs={'id': new_gorup.id})
    data = {
        'name': new_gorup.name,
        "min_age": 1,
        "max_age": 5,
        'description': new_gorup.description
    }
    resp = api_client.put(url1, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    new_g = m_models.AgeGroup.objects.get(id=new_gorup.id)
    assert new_g.min_age == 8
    assert new_g.max_age == 10

    data["min_age"] = 1
    data["max_age"] = 8

    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    old_first_group = m_models.AgeGroup.objects.get(id=first_group.id)
    assert old_first_group.min_age == 1
    assert old_first_group.max_age == 5


def test_putRequestByVendorUser(api_client, vendorUser, ageGroup, country):
    api_client.force_authenticate(vendorUser)
    text = fake.text()
    new_name = fake.name()
    data = {
        "name": new_name,
        "description": text,
        "min_age": 1,
        "max_age": 5,
        "status": 'ACTIVE',
        "country": country.name
    }
    resp = api_client.put(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == new_name
    assert first_group.description == text
    assert first_group.status == 'ACTIVE'

    # try to make new group which is already use

    new_gorup = ageGroup
    new_gorup.id = None
    new_gorup.min_age = 8
    new_gorup.max_age = 10
    new_gorup.save()

    url1 = reverse('superadmin:media_and_groupings:agegroup',
                   kwargs={'id': new_gorup.id})
    data = {
        'name': new_gorup.name,
        "min_age": 1,
        "max_age": 5,
        'description': new_gorup.description
    }
    resp = api_client.put(url1, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    new_g = m_models.AgeGroup.objects.get(id=new_gorup.id)
    assert new_g.min_age == 8
    assert new_g.max_age == 10

    data["min_age"] = 1
    data["max_age"] = 8

    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    old_first_group = m_models.AgeGroup.objects.get(id=first_group.id)
    assert old_first_group.min_age == 1
    assert old_first_group.max_age == 5


def test_putRequestBySubAdmin(api_client, subAdmin, ageGroup, country):
    api_client.force_authenticate(subAdmin)
    text = fake.text()
    new_name = fake.name()
    data = {
        "name": new_name,
        "description": text,
        "min_age": 1,
        "max_age": 5,
        "status": 'ACTIVE',
        "country": country.name
    }
    resp = api_client.put(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == new_name
    assert first_group.description == text
    assert first_group.status == 'ACTIVE'

    # try to make new group which is already use

    new_gorup = ageGroup
    new_gorup.id = None
    new_gorup.min_age = 8
    new_gorup.max_age = 10
    new_gorup.save()

    url1 = reverse('superadmin:media_and_groupings:agegroup',
                   kwargs={'id': new_gorup.id})
    data = {
        'name': new_gorup.name,
        "min_age": 1,
        "max_age": 5,
        'description': new_gorup.description
    }
    resp = api_client.put(url1, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    new_g = m_models.AgeGroup.objects.get(id=new_gorup.id)
    assert new_g.min_age == 8
    assert new_g.max_age == 10

    data["min_age"] = 1
    data["max_age"] = 8

    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    old_first_group = m_models.AgeGroup.objects.get(id=first_group.id)
    assert old_first_group.min_age == 1
    assert old_first_group.max_age == 5


def test_putRequestBySuperAdmin(api_client, superAdmin, ageGroup, country):
    api_client.force_authenticate(superAdmin)
    text = fake.text()
    new_name = fake.name()
    data = {
        "name": new_name,
        "description": text,
        "min_age": 1,
        "max_age": 5,
        "status": 'ACTIVE',
        "country": country.name
    }
    resp = api_client.put(url, data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    first_group = m_models.AgeGroup.objects.all().first()
    assert first_group.name == new_name
    assert first_group.description == text
    assert first_group.status == 'ACTIVE'

    # try to make new group which is already use

    new_gorup = ageGroup
    new_gorup.id = None
    new_gorup.min_age = 8
    new_gorup.max_age = 10
    new_gorup.save()

    url1 = reverse('superadmin:media_and_groupings:agegroup',
                   kwargs={'id': new_gorup.id})
    data = {
        'name': new_gorup.name,
        "min_age": 1,
        "max_age": 5,
        'description': new_gorup.description
    }
    resp = api_client.put(url1, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    new_g = m_models.AgeGroup.objects.get(id=new_gorup.id)
    assert new_g.min_age == 8
    assert new_g.max_age == 10

    data["min_age"] = 1
    data["max_age"] = 8

    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    old_first_group = m_models.AgeGroup.objects.get(id=first_group.id)
    assert old_first_group.min_age == 1
    assert old_first_group.max_age == 5


def test_deleteRequestByUser(api_client, user, ageGroup, country):
    api_client.force_authenticate(user)
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT


def test_deleteRequestByVendorUser(api_client, vendorUser, ageGroup, country):
    api_client.force_authenticate(vendorUser)
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT


def test_deleteRequestBySuperAdmin(api_client, superAdmin, ageGroup, country):
    api_client.force_authenticate(superAdmin)
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    url1 = reverse('superadmin:media_and_groupings:agegroup',
                   kwargs={'id': 10})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
