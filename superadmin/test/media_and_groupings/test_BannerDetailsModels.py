import pytest
import datetime
from faker import Faker
from superadmin.subapps.media_and_groupings.models import VendorBannerDetails, Marketing, Category

fake = Faker()

def test_createVendorBannerDetailsModel(marketing, category):
    new_banner = VendorBannerDetails(
        marketing  = marketing,
        catagory = category,
        page_visits = 100
    )
    new_banner.save()

    all_banners = VendorBannerDetails.objects.all()
    assert len(all_banners) == 1

    first_banner = all_banners.first()
    assert first_banner.marketing.id == marketing.id
    assert first_banner.catagory == category


def test_UpdateVendorBannerDetailsModel(marketing, category,vendorUser, city, vendor):

    new_marketing = Marketing(
        from_date = datetime.datetime.now(),
        to_date = datetime.datetime.now(),
        type = "BANNER",
        vendor = vendor,
        target_activity = "Fixed Time",
        city = city, 
        platform_type = 'WEB',
        status = 'ACTIVE',
        total_amount_paid = 1000,
        applied_tax_rate = 12,
        transaction_id='KAIE128491999',
        # created_by = vendorUser
    )
    new_marketing.save()
    name = fake.name()
    new_category = Category(
        name = name,
        index = 1
    )
    new_category.save()
    new_banner = VendorBannerDetails(
        marketing  = marketing,
        catagory = category,
        page_visits = 100
    )
    new_banner.save()
    all_banners = VendorBannerDetails.objects.all()
    assert len(all_banners) == 1
    first_banner = all_banners.first()
    first_banner.marketing = new_marketing
    first_banner.catagory = new_category
    first_banner.save()
    all_new_banners = VendorBannerDetails.objects.all().first()
    assert all_new_banners.marketing.id == new_marketing.id
    assert all_new_banners.catagory == new_category


def test_deleteBannerModel(marketing, category):
    new_banner = VendorBannerDetails(
        marketing  = marketing,
        catagory = category,
        page_visits = 100
    )
    new_banner.save()

    all_banners = VendorBannerDetails.objects.all()
    assert len(all_banners) == 1

    new_banner.delete()
    all_banners = VendorBannerDetails.objects.all()
    assert len(all_banners) == 0