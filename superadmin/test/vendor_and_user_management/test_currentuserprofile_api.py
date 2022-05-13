from superadmin.subapps.countries_and_cities.models import City, Country
import pytest
from django.urls import reverse
from superadmin.subapps.vendor_and_user_management.serializers import UserProfileSerializer
from superadmin.subapps.vendor_and_user_management.models import Family
from django.contrib.auth import get_user_model
User = get_user_model()


url = reverse('superadmin:vendor_and_user_management:currentuserprofile')


@pytest.mark.django_db
def test_RequestWithoutLogin(api_client, db):
    resp = api_client.get(url)
    assert resp.status_code == 401

    resp = api_client.post(url)
    assert resp.status_code == 401

    resp = api_client.put(url)
    assert resp.status_code == 401

    resp = api_client.patch(url)
    assert resp.status_code == 401

    resp = api_client.delete(url)
    assert resp.status_code == 401


def test_getrequest(api_client, user, country, city):
    user.userdetails.role = 'CONSUMER'
    user.userdetails.save()
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 200
    serializer = UserProfileSerializer(user)
    assert serializer.data == resp.data
    print(resp.data)


def test_getrequest(api_client, userDetails, country, city):
    print(userDetails)
    api_client.force_authenticate(userDetails)
    resp = api_client.get(url)
    assert resp.status_code == 200
    serializer = UserProfileSerializer(userDetails)
    assert serializer.data == resp.data
    assert resp.data['email'] == userDetails.email
    assert resp.data['city'] == city.name
    assert resp.data['country'] == country.name


def test_withfamilyGetRequest(api_client, country, city):
    user = User.objects.create_user(
        username="user@moppetto.com",
        password="password",
        email="user@moppetto.com"
    )
    user.save()

    user2 = User.objects.create_user(
        username="user2@moppetto.com",
        password="password",
        email="user2@moppetto.com"
    )
    user2.save()

    user_family = Family(
        superadmin=user,
        admin=user2,
        status='ACTIVE',
        upcoming_activities=0,
        past_activities=0
    )
    user_family.save()
    user.userdetails.gender = 'MALE'
    user.userdetails.role = 'CONSUMER'
    user.userdetails.rights = 'SUPERUSER'
    user.userdetails.country = country
    user.userdetails.city = city
    user.userdetails.family = user_family
    user.userdetails.save()

    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == 200
    serializer = UserProfileSerializer(user)
    assert serializer.data == resp.data
    assert resp.data['email'] == user.email
    assert resp.data['city'] == city.name
    assert resp.data['country'] == country.name
    assert resp.data['role'] == 'SUPERUSER'


def test_patchRequest(api_client):
    resp = api_client.patch(url, data={})
    assert resp.status_code == 401

    resp = api_client.put(url, data={})
    assert resp.status_code == 401

    resp = api_client.delete(url, data={})
    assert resp.status_code == 401


def test_patchRequestOfConsumer(api_client, userDetails):
    country = Country.objects.create(name="USA", abbr="US", status='ACTIVE')

    city = City.objects.create(name='city2', country=country, status='ACTIVE')
    data = {
        'city': city.name,
        'country': country.name,
        'dob': '1995-05-02',
        'email': 'usereew@gmail.com',
        'profile_image': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACQAAAAkCAQAAABLCVATAAAA5UlEQVRIx+3Vzw2CMBTH8e8RppAVmEAvbOMCPTGAY/QGC/gncRPtJOZ5sQQDvD7BmGjs79jy4ZU2PPjYKNmypVyG5LTIIy35fKjpGEFo7A9WOOouOwThhsdzQxB2vVlHNcX4p/fH+OTcoBp5GZKxqtzE0v7WhnFDqJ5Yqqf+JejE5R3QnowV16XQngyA9TIoMgVhCTTGzIDGmSQUOJuYBBQoyDkamAS0ASDjkGQMFUVKZwzfKFI6Yzi1SOmM6fgjpTHGexQoEoz5QoYE8yU/NjcLcvZ2pKeyN0gt3tay9Sgt+z/Gxx1bfJWigCzsjQAAAABJRU5ErkJggg=="
    }
    api_client.force_authenticate(userDetails)
    resp = api_client.patch(url, data=data)
    assert resp.status_code == 200
    assert resp.data['email'] == 'usereew@gmail.com'
    assert resp.data['city'] == 'city2'
    assert resp.data['country'] == 'USA'
    assert resp.data['dob'] == '1995-05-02'
    assert resp.data['age'] == 26
    assert resp.data['role'] == None


def test_putRequest(api_client, userDetails):
    api_client.force_authenticate(userDetails)
    resp = api_client.put(url, data={})
    assert resp.status_code == 405

    api_client.force_authenticate(userDetails)
    resp = api_client.delete(url, data={})
    assert resp.status_code == 405


# pytest test_currentuserprofile_api.py -s
