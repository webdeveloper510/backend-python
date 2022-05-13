from django.db.models.query_utils import Q
import pytest 
from faker import Faker
from superadmin.subapps.media_and_groupings.models import AdminBanner, Media, Category
from superadmin.subapps.countries_and_cities.models import City

fake = Faker()

def test_createDefaultBanner(category, city, media):
    admin_banner = AdminBanner(
        platform_type = "WEB",
        category = category,
        city = city,
        media = media
    )
    admin_banner.save()
    all_admin_banner = AdminBanner.objects.all()
    assert len(all_admin_banner) == 1
    assert all_admin_banner[0].platform_type == 'WEB'
    assert all_admin_banner[0].category == category
    assert all_admin_banner[0].city == city
    assert all_admin_banner[0].media == media


def test_updateDefaultBanner(category, city, media, country):
    admin_banner = AdminBanner(
        platform_type = "WEB",
        category = category,
        city = city,
        media = media
    )
    admin_banner.save()
    all_admin_banner = AdminBanner.objects.all()
    assert len(all_admin_banner) == 1
    all_admin_banner = all_admin_banner.first()
    assert all_admin_banner.platform_type == 'WEB'
    assert all_admin_banner.category == category
    assert all_admin_banner.city == city
    assert all_admin_banner.media == media


    name= fake.name()
    new_media = Media(
        name = name,
        status = 'ACTIVE',
        type = 'Image',
        used_for = 'CATEGORY_IMAGE'
    )
    new_media.save()

    new_city = City.objects.create(
        name = fake.name(),
        country = country,
        status = 'ACTIVE'
    )

    new_category = Category.objects.create(
        name = fake.name(),
        index = 2,
        status = 'ACTIVE'
    )

    all_admin_banner.platform_type = 'APP'
    all_admin_banner.category = new_category
    all_admin_banner.city = new_city
    all_admin_banner.media = new_media
    all_admin_banner.save()
    
    first_admin_banner = AdminBanner.objects.all().first()
    assert first_admin_banner.platform_type == 'APP'
    assert first_admin_banner.category == new_category
    assert first_admin_banner.city == new_city
    assert first_admin_banner.media == new_media


def test_deleteDefaultBanner(category, city):
    name = fake.name()
    new_media = Media.objects.create(
        name = name,
        status = 'ACTIVE',
        type = 'Image',
        used_for = 'CATEGORY_IMAGE'
    )

    all_media = Media.objects.all()
    assert len(all_media) == 1
    new_media.delete()

    all_media = Media.objects.all()
    assert len(all_media) == 0
