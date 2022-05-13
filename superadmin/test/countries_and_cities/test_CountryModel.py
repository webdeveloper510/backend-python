import pytest

from django.core.exceptions import ValidationError
# from django.db.models.aggregates import Count
# from rest_framework.test import APITestCase
from superadmin.subapps.countries_and_cities.models import Country
from django.db.transaction import atomic
from django.db import IntegrityError


# class CountryModelTest(APITestCase):
@pytest.mark.django_db
def test_someCase():
    '''
        Testing with all field
    '''
    country = Country.objects.create(
        name="India",
        abbr="India",
        status = 'INACTIVE'
    )
    totalCountrys = Country.objects.all().count()
    assert totalCountrys == 1
    assert country.status == 'INACTIVE'


@pytest.mark.django_db
def test_defaultValues():
    '''
        Testing with all field
    '''
    country = Country.objects.create(
        name="India"
    )
    assert country.status == 'INACTIVE'
    assert country.abbr == None


@pytest.mark.django_db
def test_nameUniqueness():
    # trying to create same name two instance 
    Country.objects.create(
        name="India",
        abbr="India"
    )
    # with atomic():
    with pytest.raises(IntegrityError):
        Country.objects.create(
            name="India",
            abbr="India"
        )

@pytest.mark.django_db
def test_withoutName():
    # trying to add country without name
    # with atomic():
    with pytest.raises(ValidationError):
        Country.objects.create(
            abbr="India",
        )

@pytest.mark.django_db
def test_ordering():
    # checking order of table data
    Country.objects.create(
        name="India",
    )
    Country.objects.create(
        name="USA",
    )
    first_country = Country.objects.all().first()
    assert "India" == first_country.name

@pytest.mark.django_db
def test_updateCountryName():

    country = Country.objects.create(
        name="India"
    )
    country.name="Japan"
    country.save()
    assert country.name == 'Japan'

@pytest.mark.django_db
def test_countryDelete():
    Country.objects.create(
        name="India"
    )
    all_country = Country.objects.all().count()
    assert all_country == 1
    Country.objects.all().delete()
    all_country = Country.objects.all().count()
    assert all_country == 0

    
