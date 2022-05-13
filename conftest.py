import pytest
from faker import Faker
from django.contrib.auth import get_user_model
User = get_user_model()
from superadmin.subapps.countries_and_cities.models import Country, City, Region, Area
from rest_framework.test import APIClient
# Vendor, VendorDetails, Family
from superadmin.subapps.vendor_and_user_management import models as userModels


fake = Faker()


@pytest.fixture
def country(db):
    country = Country(
        name="India",
        abbr="IN",
        status="ACTIVE"
    )

    country.save()
    return country


@pytest.fixture
def city(country):
    new_city = City.objects.create(
        name="Kolkata",
        country=country,
        status='ACTIVE'
    )
    return new_city


@pytest.fixture
def region(city):
    new_region = Region.objects.create(
        name="Egipura",
        city=city,
        status="INACTIVE"
    )
    return new_region


@pytest.fixture
def area(region):
    area = Area.objects.create(
        name="Sector V",
        region=region,
        status="ACTIVE"
    )
    return area


@pytest.fixture
def api_client():
    apiClient = APIClient()
    return apiClient


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        username="user@moppetto.com",
        password="password",
        email="user@moppetto.com"
    )
    user.save()
    return user


@pytest.fixture
def subAdmin(db):
    subAdmin = User.objects.create_user(
        username="staffs@moppetto.com",
        email="staffs@moppetto.com",
        password="password",
        is_staff=True
    )
    return subAdmin


@pytest.fixture
def superAdmin(db):
    superAdmin = User.objects.create_superuser(
        username="superadmin@moppetto.com",
        email="superadmin@moppetto.com",
        password="password",
        is_staff=True,
        is_superuser=True
    )
    return superAdmin


@pytest.fixture
def vendorUser(db):
    vendorUser = User.objects.create_user(
        username="vendor@moppetto.com",
        email="vendor@moppetto.com",
        password="password",
        first_name="Vendor",
        last_name="Vendor"
    )

    return vendorUser


@pytest.fixture
def vendor(vendorUser, country, city):
    new_vendor = userModels.Vendor(
        user=vendorUser,
        vendor_code="1234",
        name="Vendor vendor",
        email="vendor@moppetto.com",
        organization_type="INDIVIDUAL",
        status="ACTIVE",
        vendor_status="VENDOR",
        country=country,
        city=city
    )
    new_vendor.save()
    return new_vendor




@pytest.fixture
def vendorDetails(vendor):
    vd = userModels.VendorDetails(
        vendor=vendor,
        legal_name="vendor",
        entity_reg_number="",
        profile_intro=fake.text(),
        terms=fake.text(),
    )
    vd.save()

    return vd


@pytest.fixture
def userDetails(user, country, city):
    user.userdetails.gender = 'MALE'
    user.userdetails.role = 'CONSUMER'
    user.userdetails.rights = 'SUPERUSER'
    user.userdetails.country = country
    user.userdetails.city = city
    user.userdetails.code = 'User2010'
    user.userdetails.save()
    return user


@pytest.fixture
def userFamily(user, country, city):
    family = userModels.Family.objects.create(
        superadmin=user,
        status='ACTIVE'
    )
    user.userdetails.gender = 'MALE'
    user.userdetails.role = 'CONSUMER'
    user.userdetails.rights = 'SUPERUSER'
    user.userdetails.country = country
    user.userdetails.city = city
    user.userdetails.family = family
    user.userdetails.save()
    return user


@pytest.fixture
def userKids(user, country, city):
    family = userModels.Family.objects.create(
        superadmin=user,
        status='ACTIVE'
    )
    user.userdetails.gender = 'MALE'
    user.userdetails.role = 'CONSUMER'
    user.userdetails.rights = 'SUPERUSER'
    user.userdetails.country = country
    user.userdetails.city = city
    user.userdetails.family = family
    user.userdetails.save()

    return userModels.Kid.objects.create(
        first_name='kid1',
        last_name='last',
        family=family
    )
