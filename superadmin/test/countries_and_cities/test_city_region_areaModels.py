import pytest
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from superadmin.subapps.countries_and_cities.models import City, Country, Region, Area
from django.contrib.auth import get_user_model
User = get_user_model()


#  city model test start
def test_city_creation(country):
    new_city = City.objects.create(
        name = 'Pune',
        country = country,
        status = "ACTIVE",
        # created_by = self.user,
    )
    all_cities = City.objects.all().count()
    assert all_cities == 1
    assert new_city.name == 'Pune'
    assert new_city.country.name == 'India'
    assert new_city.status == 'ACTIVE'


def test_city_creating_without_name(country):
    # with atomic():
        with pytest.raises(ValidationError):
            City.objects.create(
                country = country,
                status = "ACTIVE",
                # created_by = self.user,
            )

    # with atomic():
        with pytest.raises(ValidationError):
            City.objects.create(
                name="Kolkata",
                status = "ACTIVE",
                # created_by = self.user,
            )

def test_tryToDeleteCountry(country):
    # with atomic():
    City.objects.create(
        name = 'Mumbai',
        country = country,
        status = "ACTIVE",
        # created_by = cls.user,
    )
    with pytest.raises(IntegrityError):
        Country.objects.get(name="India").delete()
    
def test_updatingCity(city):
    user = User.objects.create(
        username="test2",
        email="test2@moppetto.com",
        password='1234'
    )

    city.name = 'Bangalore'
    city.save()
    assert city.name == 'Bangalore'
    
    city.updated_by = user
    city.save()
    assert city.updated_by == user

@pytest.mark.django_db
def test_deletion():
    new_country = Country.objects.create(
        name="USA",
        abbr="US",
        status='ACTIVE'
    )

    city = City.objects.create(
        name = 'Kolkata',
        country = new_country,
        status = "ACTIVE"
    )
    
    assert city.country.name == "USA"
    # with atomic():
    with pytest.raises(ProtectedError):
        Country.objects.get(name="USA").delete()
    city.delete()
    Country.objects.get(name="USA").delete()
    

# city model test end #

# Region model test start #

def test_region_creation(city):
    new_region = Region.objects.create(
        name = "Metropolitan",
        city = city,
        status = "INACTIVE"
    )
    assert new_region.name ==  "Metropolitan"
    assert new_region.status ==  "INACTIVE"
    assert new_region.city ==  city


def test_region_update(country, city):
    new_city = City.objects.create(
        name="bangalore",
        country=country,
        status = "ACTIVE"
    )
    new_region = Region.objects.create(
        name = "Metropolitan",
        city = city,
        status = "INACTIVE"
    )
    new_region.name = 'xyz'
    new_region.status = "ACTIVE"
    new_region.city = new_city
    new_region.save()
    assert new_region.name == 'xyz'
    assert new_region.status == "ACTIVE"
    assert new_region.city == new_city


def test_region_deleteion(city):
    new_region = Region.objects.create(
        name = "Metropolitan",
        city = city,
        status = "INACTIVE"
    )
    new_region.delete()

def test_city_delete_where_regioun_is_used(country, city):
    # when region is use the city 
    new_region = Region.objects.create(
        name = "Metropolitan",
        city = city,
        status = "INACTIVE"
    )
    # with atomic():
    with pytest.raises(ProtectedError):
        city.delete()
    
    with pytest.raises(ProtectedError):
        country.delete()

def test_creating_regionWithoutName(city):
    with pytest.raises(ValidationError):
        Region.objects.create(
            city = city,
            status = "INACTIVE"
        )

def test_creating_regionLessThenThreeCharecters(city):
    with pytest.raises(ValidationError):
        Region.objects.create(
            name="mn",
            city = city,
            status = "INACTIVE"
        )

# Region model test complete

# Area model test start 
def test_area_creating(region):
    new_area = Area.objects.create(
        name = "Sector V",
        region = region,
        status = "ACTIVE"
    )

    assert new_area.name == "Sector V"
    assert new_area.region == region
    assert new_area.status == "ACTIVE"

def test_area_name(region):
    # give validation error when there not be name and name will not be three charecters  
    with pytest.raises(ValidationError):
        Area.objects.create(
            region = region,
            status = "ACTIVE"
        )
    
    with pytest.raises(ValidationError):
        Area.objects.create(
            name='ab',
            region = region,
            status = "ACTIVE"
        )
    
def test_area_update(region):
    area = Area.objects.create(
                name="asdfr",
                region = region,
                status = "ACTIVE"
            )
    area.name= "lsutr"
    area.save()
    area.name='ps'
    with pytest.raises(ValidationError):
        area.save()
        


def test_try_to_delete_region(region, city, country):
    Area.objects.create(
        name='abc',
        region = region,
        status = "ACTIVE"
    )

    with pytest.raises(IntegrityError):
        region.delete()
    with pytest.raises(IntegrityError):
        city.delete()
    with pytest.raises(IntegrityError):
        country.delete()
    

