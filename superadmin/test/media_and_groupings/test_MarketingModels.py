import pytest
from faker import Faker
import datetime
from superadmin.subapps.media_and_groupings.models import Marketing

# @pytest.mark.django_db
def test_MarketingModel(vendorUser, city, vendor):
    marketing = Marketing(
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
    marketing.save()

    all_marketing = Marketing.objects.all()
    assert len(all_marketing) == 1
    assert all_marketing[0].type == "BANNER"
    assert all_marketing[0].vendor == vendor
    assert all_marketing[0].target_activity == "Fixed Time"
    assert all_marketing[0].platform_type =='WEB'
    assert all_marketing[0].transaction_id == 'KAIE128491999'
    assert all_marketing[0].status == 'ACTIVE'
    assert all_marketing[0].city == city

def test_MarketingModelUpdate(vendorUser, city, vendor):
    marketing = Marketing(
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
    marketing.save()

    all_marketing = Marketing.objects.all()
    all_marketing[0].type = "TRENDING"
    all_marketing[0].target_activity = "Day Access"
    all_marketing[0].platform_type ='APP'
    all_marketing[0].transaction_id = '7894555'
    all_marketing[0].status = 'SUSPENDED'
    all_marketing[0].save()

    firstMarketing = Marketing.objects.all().first()
    firstMarketing.type == "TRENDING"
    firstMarketing.target_activity == "Day Access"
    firstMarketing.platform_type =='APP'
    firstMarketing.transaction_id == '7894555'
    firstMarketing.status == 'SUSPENDED'

def test_deleteOfMarketingModel(vendorUser, city, vendor):
    marketing = Marketing(
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
    marketing.save()
    all_marketing = Marketing.objects.all()
    assert len(all_marketing) == 1

    marketing.delete()

    _all_marketing = Marketing.objects.all()
    assert len(_all_marketing) == 0