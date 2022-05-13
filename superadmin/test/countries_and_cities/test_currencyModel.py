import pytest
from superadmin.subapps.countries_and_cities.models import Currency, Country
from django.db import IntegrityError


def test_currencyCreate(country):
    Currency.objects.create(
        country=country,
        display_character='$',
        name="dollrs"
    )
    totalCurrency = Currency.objects.all().count()
    assert totalCurrency == 1

#    
def test_currencyUniqueness(country):
    Currency.objects.create(
        country=country,
        display_character='$',
        name="dollrs"
    )

    with pytest.raises(IntegrityError):
        Currency.objects.create(
            country=country,
            display_character='$',
            name="dollrs"
        )



