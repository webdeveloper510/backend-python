from rest_framework import status
from superadmin.subapps.media_and_groupings.views_age_groups import AgeGroups
import pytest
from faker import Faker
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

from superadmin.subapps.media_and_groupings.models import (
    Category, Attribute, Marketing, Media, SubAttribute,
    AgeGroup, VendorBannerDetails, AdminBanner,
    SubCategory, HeaderDetails, DefaultHeader, Avatar,
    Media
)

from superadmin.subapps.vendor_and_user_management import models as vendorAndUserModels


fake = Faker()


@pytest.fixture
def category(db):
    category = Category(
        name=fake.name()
    )
    category.save()
    return category


@pytest.fixture
def subCategory(category):
    subCategory = SubCategory(
        name=fake.name(),
        category=category
    )
    subCategory.save()
    return subCategory


@pytest.fixture
def attribute(superAdmin):
    attr = Attribute(
        name=fake.name(),
    )
    attr.save()
    return attr


@pytest.fixture
def subAttributes(attribute):
    subAttr = SubAttribute(
        name='SubAttr1',
        attribute=attribute
    )
    subAttr.save()
    return subAttr


@pytest.fixture
def marketing(vendorUser, city, vendor):
    new_marketing = Marketing(
        from_date=datetime.datetime.now(),
        to_date=datetime.datetime.now(),
        type="BANNER",
        vendor=vendor,
        target_activity="Fixed Time",
        city=city,
        platform_type='WEB',
        status='ACTIVE',
        total_amount_paid=1000,
        applied_tax_rate=12,
        transaction_id='KAIE128491999'
    )

    new_marketing.save()
    return new_marketing


@pytest.fixture
def bannerDetails(marketing, category):
    banner = VendorBannerDetails(
        marketing=marketing,
        catagory=category,
        page_visits=1,

    )
    banner.save()
    return banner


@pytest.fixture
def HeaderMarketing(vendorUser, city, vendor):
    new_marketing = Marketing(
        from_date=datetime.datetime.now(),
        to_date=datetime.datetime.now(),
        type="HEADER",
        vendor=vendor,
        target_activity="Fixed Time",
        city=city,
        platform_type='WEB',
        status='ACTIVE',
        total_amount_paid=1000,
        applied_tax_rate=12,
        transaction_id='KAIE128491999'
    )
    new_marketing.save()
    return new_marketing


@pytest.fixture
def headerDetails(HeaderMarketing):
    headerDetails = HeaderDetails(
        marketing=HeaderMarketing,
        page_visits=100,
        text="some texts"
    )
    headerDetails.save()
    return headerDetails


@pytest.fixture
def media(db):
    name = fake.name()
    new_media = Media(
        name=name,
        file=SimpleUploadedFile(
            'gst.jpeg', b"file_content", content_type="image/jpeg")
    )
    new_media.save()
    return new_media


@pytest.fixture
def ageGroup(country):
    ageGroups = AgeGroup(
        name="Baby Groups",
        min_age=1,
        max_age=3,
        status='INACTIVE',
        country=country
    )
    ageGroups.save()
    return ageGroups


@pytest.fixture
def defaultBanner(category, city):
    defaultBanners = AdminBanner(
        platform_type="WEB",
        category=category,
        city=city
    )
    defaultBanners.save()
    return defaultBanner


@pytest.fixture
def defaultHeader(category, city):
    defaultHeader = DefaultHeader(
        date=datetime.datetime.now(),
        city=city,
        platform_type='WEB',
        text=fake.text()
    )
    defaultHeader.save()
    return defaultHeader


@pytest.fixture
def avatars(db):
    boy_avatar = Avatar(
        name='Avatar1',
        type='BOY',
        status='ACTIVE'
    )
    girl_avatar = Avatar(
        name='Avatar1',
        type='GIRL',
        status='ACTIVE'
    )
    boy_avatar.save()
    girl_avatar.save()
    return boy_avatar


@pytest.fixture
def avatar(db, media):
    boy_avatar = Avatar(
        name='Avatar1',
        type='BOY',
        status='ACTIVE',
        media=media
    )
    boy_avatar.save()
    return boy_avatar


@pytest.fixture
def kid(db, avatar):
    kids = vendorAndUserModels.Kid(
        first_name='Kid1',
        last_name='last',
        dob='2020-01-01',
        avatar=avatar
    )
    kid.save()
    return kids
