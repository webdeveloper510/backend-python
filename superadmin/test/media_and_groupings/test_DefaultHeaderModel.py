from datetime import date
import pytest
from faker import Faker
from datetime import date
from superadmin.subapps.media_and_groupings.models import DefaultHeader

fake = Faker()

def test_createDefaultHeader(city):
    texts = fake.text()
    DefaultHeader.objects.create(
        date = date.today(),
        city = city,
        platform_type = 'WEB',
        text = texts
    )
    all_default_header = DefaultHeader.objects.all()
    assert  len(all_default_header) == 1

    assert all_default_header[0].text == texts
    assert all_default_header[0].platform_type == 'WEB'


def test_updateDefaultHeader(city):
    texts = fake.text()
    DefaultHeader.objects.create(
        date = date.today(),
        city = city,
        platform_type = 'WEB',
        text = texts
    )
    all_default_header = DefaultHeader.objects.all()
    assert  len(all_default_header) == 1

    assert all_default_header[0].text == texts
    assert all_default_header[0].platform_type == 'WEB'

    new_city = city
    new_city.id = None
    new_city.name = fake.name()
    new_city.save()

    new_text = fake.text()
    all_default_header[0].text = new_text
    all_default_header[0].city = new_city
    all_default_header[0].platform_type = 'APP'
    all_default_header[0].save()


    all_default_header = DefaultHeader.objects.all()

    assert all_default_header[0].text == new_text
    assert all_default_header[0].platform_type == 'APP'
    assert all_default_header[0].city == new_city


def test_deleteDefaultHeader(city):
    texts = fake.text()
    DefaultHeader.objects.create(
        date = date.today(),
        city = city,
        platform_type = 'WEB',
        text = texts
    )
    all_default_header = DefaultHeader.objects.all()
    assert  len(all_default_header) == 1

    all_default_header[0].delete()
    
    all_default_header = DefaultHeader.objects.all()
    assert  len(all_default_header) == 0
