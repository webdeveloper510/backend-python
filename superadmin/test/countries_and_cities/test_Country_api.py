import pytest
from django.urls.base import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import status
from superadmin.subapps.countries_and_cities.models import Country, City, Area, Region
from superadmin.subapps.countries_and_cities.serializers import CountrySerializer, CountryCompactSerializer
from superadmin.subapps.vendor_and_user_management.models import Vendor

url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':1})


# def postRequestBySuperUser(self):
#     self.client.force_authenticate(user=self.superAdmin)
#     resp = self.client.post(self.addCountryDataUrl, data=self.data, format='json')
#     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

def test_getRequestWithoutLogin(api_client, country):
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    country_obj = Country.objects.get(id=1, status='ACTIVE')
    serializer = CountrySerializer(country_obj)
    assert resp.data == serializer.data
    

def test_getCountryDetailsByUser(api_client, user, country):
    api_client.force_authenticate(user)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    country_obj = Country.objects.get(id=1, status='ACTIVE')
    serializer = CountrySerializer(country_obj)
    assert resp.data == serializer.data

def test_getCountryDetailsBySubAdmin(api_client, subAdmin, country):
    # self.postRequestBySuperUser()
    api_client.force_authenticate(subAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    country_obj = Country.objects.get(id=1, status='ACTIVE')
    serializer = CountrySerializer(country_obj)
    assert resp.data == serializer.data
    
def test_getCountryDetailsBySuperAdmin(api_client,country, superAdmin):
    api_client.force_authenticate(superAdmin)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    country_obj = Country.objects.get(id=1, status='ACTIVE')
    serializer = CountrySerializer(country_obj)
    assert resp.data == serializer.data
    
def test_getCountryDetailsByVendor(api_client,country, vendorUser):
    api_client.force_authenticate(vendorUser)
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    country_obj = Country.objects.get(id=1, status='ACTIVE')
    serializer = CountrySerializer(country_obj)
    assert resp.data == serializer.data

def test_getCountryDetailsWrongIDByUser(api_client, user, country):
    api_client.force_authenticate(user)
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    

def test_getCountryDetailsWrongIDBySuperAdmin(api_client, superAdmin, country):
    api_client.force_authenticate(superAdmin)
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
def test_getCountryDetailsWrongIDByVendor(api_client, vendorUser, country):
    api_client.force_authenticate(vendorUser)
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':10})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    
def test_post_requestForVendor(api_client, vendorUser, country):
    api_client.force_authenticate(vendorUser)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    

def test_post_requestForUser(api_client, user, country):
    api_client.force_authenticate(user)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    

def test_post_requestForsubAdmin(api_client, subAdmin, country):
    api_client.force_authenticate(subAdmin)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    
def test_post_requestForAdmin(api_client, superAdmin, country):
    api_client.force_authenticate(superAdmin)
    resp = api_client.post(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_put_requestForVendor(api_client, vendorUser, country):
    api_client.force_authenticate(vendorUser)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    

def test_put_requestForUser(api_client, user, country):
    api_client.force_authenticate(user)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    
    
def test_put_requestForsubAdmin(api_client, subAdmin, country):
    api_client.force_authenticate(subAdmin)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    
def test_put_requestForAdmin(api_client, superAdmin, country):
    api_client.force_authenticate(superAdmin)
    resp = api_client.put(url)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
def test_delete_withoutLogin(api_client, country, city):
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    country2= Country.objects.create(name="INDIAN", abbr='IN',status="ACTIVE")
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':country2.id})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    
def test_delete_by_user(api_client, user, country, city):
    api_client.force_authenticate(user)
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    country2= Country.objects.create(name="INDIAN", abbr='IN',status="ACTIVE")
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':country2.id})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT

def test_delete_bySubAdmin(api_client, subAdmin, country, city):
    api_client.force_authenticate(subAdmin)
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    country2= Country.objects.create(name="INDIAN", abbr='IN',status="ACTIVE")
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':country2.id})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    
def test_delete_bySuperAdmin(api_client, superAdmin, country, city):
    api_client.force_authenticate(superAdmin)
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    country2= Country.objects.create(name="INDIAN", abbr='IN',status="ACTIVE")
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':country2.id})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    
def test_delete_byVendor(api_client, vendorUser, country, city):
    api_client.force_authenticate(vendorUser)
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':1})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    country2= Country.objects.create(name="INDIAN", abbr='IN',status="ACTIVE")
    url = reverse("superadmin:countries_and_cities:Country", kwargs={'id':country2.id})
    resp = api_client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT

def test_patchRequestWithoutLogin(api_client, country, city, region, area):
    data = {
        "name": 'ASDF'
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    country = Country.objects.filter(id=1, status="ACTIVE").first()
    assert country.name =='ASDF'
    firstCity = City.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id,
            'name': "Cities1",
            'status': "INACTIVE"
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    city = City.objects.get(id=firstCity.id)
    assert city.name == "Cities1"
    assert city.status == "INACTIVE"

    new_country = Country.objects.create(name="Country2", status="ACTIVE", abbr='Counts')
    data = {
        "cities": [{
            'id': firstCity.id,
            'country': new_country.id
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    city = City.objects.get(id=firstCity.id)
    assert city.country.id != new_country.id
    assert city.country.id == 1

    data = {
        "cities": [{
            'id': 10, # id does not exist
            'name': "city2"
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data = {
        "cities": [{
            'id': firstCity.id, 
            'name': "ct"
        }],
    }

    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    firstRegion = Region.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'name': 'Region2'
                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert resp.status_code == status.HTTP_200_OK
    assert reg.name == 'Region2'

    firstRegion = Region.objects.all().first()
    city3 = City.objects.create(name='City3', country=country, status='ACTIVE')
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'name': 'Re',
                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert reg.name == firstRegion.name
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'city': city3.id

                }
            ]
        }],
    }
    api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert reg.city.id == firstRegion.city.id
    
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': {
                        "name":"KDJF"
                    }

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    area=Area.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': [{
                        "id":area.id,
                        "name":"KDJF"
                    }]

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    area=Area.objects.get(id=area.id)
    assert area.name == "KDJF"
    
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': [{
                        "id":area.id,
                        "name":"KD"
                    }]

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    area=Area.objects.get(id=area.id)
    assert area.name == "KDJF"




def test_patch_by_user(api_client, user, country, city, region, area):
    api_client.force_authenticate(user)
    data = {
        "name": 'ASDF'
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    country = Country.objects.filter(id=1, status="ACTIVE").first()
    assert country.name =='ASDF'
    firstCity = City.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id,
            'name': "Cities1",
            'status': "INACTIVE"
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    city = City.objects.get(id=firstCity.id)
    assert city.name == "Cities1"
    assert city.status == "INACTIVE"

    new_country = Country.objects.create(name="Country2", status="ACTIVE", abbr='Counts')
    data = {
        "cities": [{
            'id': firstCity.id,
            'country': new_country.id
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    city = City.objects.get(id=firstCity.id)
    assert city.country.id != new_country.id
    assert city.country.id == 1

    data = {
        "cities": [{
            'id': 10, # id does not exist
            'name': "city2"
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data = {
        "cities": [{
            'id': firstCity.id, 
            'name': "ct"
        }],
    }

    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    firstRegion = Region.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'name': 'Region2'
                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert resp.status_code == status.HTTP_200_OK
    assert reg.name == 'Region2'

    firstRegion = Region.objects.all().first()
    city3 = City.objects.create(name='City3', country=country, status='ACTIVE')
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'name': 'Re',
                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert reg.name == firstRegion.name
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'city': city3.id

                }
            ]
        }],
    }
    api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert reg.city.id == firstRegion.city.id
    
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': {
                        "name":"KDJF"
                    }

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    area=Area.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': [{
                        "id":area.id,
                        "name":"KDJF"
                    }]

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    area=Area.objects.get(id=area.id)
    assert area.name == "KDJF"
    
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': [{
                        "id":area.id,
                        "name":"KD"
                    }]

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    area=Area.objects.get(id=area.id)
    assert area.name == "KDJF"



def test_patch_byVendor(api_client, vendorUser, country, city, region, area ):
    api_client.force_authenticate(vendorUser)
    data = {
        "name": 'ASDF'
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    country = Country.objects.filter(id=1, status="ACTIVE").first()
    assert country.name =='ASDF'
    firstCity = City.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id,
            'name': "Cities1",
            'status': "INACTIVE"
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    city = City.objects.get(id=firstCity.id)
    assert city.name == "Cities1"
    assert city.status == "INACTIVE"

    new_country = Country.objects.create(name="Country2", status="ACTIVE", abbr='Counts')
    data = {
        "cities": [{
            'id': firstCity.id,
            'country': new_country.id
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    city = City.objects.get(id=firstCity.id)
    assert city.country.id != new_country.id
    assert city.country.id == 1

    data = {
        "cities": [{
            'id': 10, # id does not exist
            'name': "city2"
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data = {
        "cities": [{
            'id': firstCity.id, 
            'name': "ct"
        }],
    }

    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    firstRegion = Region.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'name': 'Region2'
                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert resp.status_code == status.HTTP_200_OK
    assert reg.name == 'Region2'

    firstRegion = Region.objects.all().first()
    city3 = City.objects.create(name='City3', country=country, status='ACTIVE')
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'name': 'Re',
                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert reg.name == firstRegion.name
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'city': city3.id

                }
            ]
        }],
    }
    api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert reg.city.id == firstRegion.city.id
    
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': {
                        "name":"KDJF"
                    }

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    area=Area.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': [{
                        "id":area.id,
                        "name":"KDJF"
                    }]

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    area=Area.objects.get(id=area.id)
    assert area.name == "KDJF"
    
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': [{
                        "id":area.id,
                        "name":"KD"
                    }]

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    area=Area.objects.get(id=area.id)
    assert area.name == "KDJF"
    
def test_patchBySubAdmin(api_client, subAdmin, country, city, region, area):
    data = {
        "name": 'ASDF'
    }
    api_client.force_authenticate(subAdmin)
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    country = Country.objects.filter(id=1, status="ACTIVE").first()
    assert country.name =='ASDF'
    firstCity = City.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id,
            'name': "Cities1",
            'status': "INACTIVE"
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    city = City.objects.get(id=firstCity.id)
    assert city.name == "Cities1"
    assert city.status == "INACTIVE"

    new_country = Country.objects.create(name="Country2", status="ACTIVE", abbr='Counts')
    data = {
        "cities": [{
            'id': firstCity.id,
            'country': new_country.id
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    city = City.objects.get(id=firstCity.id)
    assert city.country.id != new_country.id
    assert city.country.id == 1

    data = {
        "cities": [{
            'id': 10, # id does not exist
            'name': "city2"
        }],
    }
    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    data = {
        "cities": [{
            'id': firstCity.id, 
            'name': "ct"
        }],
    }

    resp = api_client.patch(url, data=data, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    firstRegion = Region.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'name': 'Region2'
                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert resp.status_code == status.HTTP_200_OK
    assert reg.name == 'Region2'

    firstRegion = Region.objects.all().first()
    city3 = City.objects.create(name='City3', country=country, status='ACTIVE')
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'name': 'Re',
                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert reg.name == firstRegion.name
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'city': city3.id

                }
            ]
        }],
    }
    api_client.patch(url, data=data, format='json')
    reg =Region.objects.get(id=firstRegion.id)
    assert reg.city.id == firstRegion.city.id
    
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': {
                        "name":"KDJF"
                    }

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    area=Area.objects.all().first()
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': [{
                        "id":area.id,
                        "name":"KDJF"
                    }]

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_200_OK
    area=Area.objects.get(id=area.id)
    assert area.name == "KDJF"
    
    data = {
        "cities": [{
            'id': firstCity.id, # id does not exist
            "regions":[
                {
                    'id': firstRegion.id,
                    'areas': [{
                        "id":area.id,
                        "name":"KD"
                    }]

                }
            ]
        }],
    }
    resp = api_client.patch(url, data=data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    area=Area.objects.get(id=area.id)
    assert area.name == "KDJF"

    
    
def test_patchBySuperAdmin(api_client, superAdmin, country, city, region, area):
        data = {
            "name": 'ASDF'
        }
        api_client.force_authenticate(superAdmin)
        resp = api_client.patch(url, data=data, format="json")
        assert resp.status_code == status.HTTP_200_OK
        country = Country.objects.filter(id=1, status="ACTIVE").first()
        assert country.name == 'ASDF'
        firstCity = City.objects.all().first()
        data = {
            "cities": [{
                'id': firstCity.id,
                'name': "Cities1",
                'status': "INACTIVE"
            }],
        }
        resp = api_client.patch(url, data=data, format="json")
        assert resp.status_code == status.HTTP_200_OK
        city = City.objects.get(id=firstCity.id)
        assert city.name =="Cities1"
        assert city.status == "INACTIVE"

        new_country = Country.objects.create(name="Country2", status="ACTIVE", abbr='Counts')
        data = {
            "cities": [{
                'id': firstCity.id,
                'country': new_country.id
            }],
        }
        resp = api_client.patch(url, data=data, format="json")
        assert resp.status_code == status.HTTP_200_OK
        city = City.objects.get(id=firstCity.id)
        assert city.country.id != new_country.id
        assert city.country.id == 1

        data = {
            "cities": [{
                'id': 10, # id does not exist
                'name': "city2"
            }],
        }
        resp = api_client.patch(url, data=data, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        data = {
            "cities": [{
                'id': firstCity.id, # id does not exist
                'name': "ct"
            }],
        }

        resp = api_client.patch(url, data=data, format="json")
        assert resp.status_code== status.HTTP_400_BAD_REQUEST
        firstRegion = Region.objects.all().first()
        data = {
            "cities": [{
                'id': firstCity.id, # id does not exist
                "regions":[
                    {
                        'id': firstRegion.id,
                        'name': 'Region2'
                    }
                ]
            }],
        }
        resp = api_client.patch(url, data=data, format='json')
        reg =Region.objects.get(id=firstRegion.id)
        assert resp.status_code == status.HTTP_200_OK
        assert reg.name == 'Region2'

        firstRegion = Region.objects.all().first()
        city3 = City.objects.create(name='City3', country=country, status='ACTIVE')
        data = {
            "cities": [{
                'id': firstCity.id, # id does not exist
                "regions":[
                    {
                        'id': firstRegion.id,
                        'name': 'Re',
                    }
                ]
            }],
        }
        resp = api_client.patch(url, data=data, format='json')
        reg =Region.objects.get(id=firstRegion.id)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert reg.name == firstRegion.name
        data = {
            "cities": [{
                'id': firstCity.id, # id does not exist
                "regions":[
                    {
                        'id': firstRegion.id,
                        'city': city3.id

                    }
                ]
            }],
        }
        api_client.patch(url, data=data, format='json')
        reg =Region.objects.get(id=firstRegion.id)
        assert reg.city.id == firstRegion.city.id
        
        data = {
            "cities": [{
                'id': firstCity.id, # id does not exist
                "regions":[
                    {
                        'id': firstRegion.id,
                        'areas': {
                            "name":"KDJF"
                        }

                    }
                ]
            }],
        }
        resp = api_client.patch(url, data=data, format='json')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        area=Area.objects.all().first()
        data = {
            "cities": [{
                'id': firstCity.id, # id does not exist
                "regions":[
                    {
                        'id': firstRegion.id,
                        'areas': [{
                            "id":area.id,
                            "name":"KDJF"
                        }]

                    }
                ]
            }],
        }
        resp = api_client.patch(url, data=data, format='json')
        assert resp.status_code == status.HTTP_200_OK
        area=Area.objects.get(id=area.id)
        assert area.name == "KDJF"
        
        data = {
            "cities": [{
                'id': firstCity.id, # id does not exist
                "regions":[
                    {
                        'id': firstRegion.id,
                        'areas': [{
                            "id":area.id,
                            "name":"KD"
                        }]

                    }
                ]
            }],
        }
        resp = api_client.patch(url, data=data, format='json')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        area=Area.objects.get(id=area.id)
        assert area.name == "KDJF"

