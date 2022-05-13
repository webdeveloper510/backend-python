import datetime
import pytest
from superadmin.subapps.subscription_pricing.models import VendorSubscription, SubscriptionPackage
from superadmin.subapps.receipt.models import ReceiptConfig
from superadmin.subapps.media_and_groupings.models import SearchWordPricing, Marketing, SearchWordDetail
from superadmin.subapps.subscription_pricing import models as subsPriceModel
from superadmin.subapps.revenue import models as revenueModel


@pytest.fixture
def receipts(db, city):
    recepts = ReceiptConfig(
        city=city,
        tax_name='XYZ',
        tax_rate=18,
        prices_include_tax=True
    )
    recepts.save()
    return recepts


@pytest.fixture
def package(db, country):
    subscriptionPackage = SubscriptionPackage(
        subscription_type='BASIC',
        price_per_month=1000,
        price_per_year=12000,
        country=country,
        no_of_locations=5,
        no_of_subadmins=1,
        no_of_media=1,
        has_trial_class=1,
        has_promotions=1,
        has_reports=1,
        baner_credit=1,
        header_credit=1,
        search_word_credit=1,
        max_slots_dayaccess=2,
        max_slots_fixedtiming=2,
        max_slots_open=2,
        max_slots_term=2
    )
    subscriptionPackage.save()
    return subscriptionPackage


@pytest.fixture
def vendor_subscription(db, vendor, package):
    today = datetime.date.today()
    endDate = today + datetime.timedelta(days=10)
    vendorSubs = VendorSubscription(
        vendor=vendor,
        start_date=today,
        end_date=endDate,
        new_billing_date=endDate,
        unsubscribed_at=endDate,
        subscription=package,
        total_amount_paid=1000,
        applied_tax_rate=18,
        cycle_type='MONTHLY',
        status='CURRENT',
    )
    vendorSubs.save()
    return vendorSubs


@pytest.fixture
def searchWords(db, vendor, city):
    arr = [
        {'from_data': '2021-09-06', 'to_date': '2022-09-05'},
        {'from_data': '2020-09-06', 'to_date': '2021-09-05'},
        {'from_data': '2021-05-06', 'to_date': '2022-05-05'}
    ]

    words = [
        {'days': 5, "no_of_searchwords": 5, "price": 500},
        {'days': 7, "no_of_searchwords": 9, "price": 700},
        {'days': 9, "no_of_searchwords": 9, "price": 900}
    ]
    i = 0
    while i < 3:
        search_word = SearchWordPricing(
            days=words[i]['days'],
            no_of_searchwords=words[i]['no_of_searchwords'],
            price=words[i]['price']
        )
        search_word.save()

        mk_sear = Marketing(
            from_date=arr[i]['from_data'],
            to_date=arr[i]['from_data'],
            type='SEARCH_WORDS',
            vendor=vendor,
            target_activity='Day Access',
            city=city,
            platform_type='WEB',
            status='SCHEDULED',
            total_amount_paid=3650,
            applied_tax_rate=2,
            transaction_id='1233455'
        )
        mk_sear.save()

        det = SearchWordDetail(
            marketing=mk_sear,
            no_of_searchwords=words[i]['no_of_searchwords'],
            page_visits=1000
        )
        det.save()
        i += 1
    return


@pytest.fixture
def subscriptionPackages(country):
    package1 = subsPriceModel.SubscriptionPackage(
        subscription_type='ADVANCE',
        price_per_month=10,
        price_per_year=120,
        country=country,

        no_of_locations=1,
        no_of_subadmins=1,
        no_of_media=7,
        has_trial_class=True,
        has_promotions=True,
        has_reports=True,
        baner_credit=10,
        header_credit=10,
        search_word_credit=10,

        max_slots_dayaccess=10,
        max_slots_fixedtiming=10,
        max_slots_open=10,
        max_slots_term=10
    )

    package2 = SubscriptionPackage(
        subscription_type='PREMIUM',
        price_per_month=15,
        price_per_year=180,
        country=country,

        no_of_locations=5,
        no_of_subadmins=5,
        no_of_media=10,
        has_trial_class=True,
        has_promotions=True,
        has_reports=True,
        baner_credit=10,
        header_credit=10,
        search_word_credit=10,

        max_slots_dayaccess=10,
        max_slots_fixedtiming=10,
        max_slots_open=10,
        max_slots_term=10
    )
    package3 = SubscriptionPackage(
        subscription_type='ENTERPRISE',
        price_per_month=20,
        price_per_year=240,
        country=country,

        no_of_locations=10,
        no_of_subadmins=15,
        no_of_media=17,
        has_trial_class=True,
        has_promotions=True,
        has_reports=True,
        baner_credit=10,
        header_credit=10,
        search_word_credit=10,

        max_slots_dayaccess=10,
        max_slots_fixedtiming=10,
        max_slots_open=10,
        max_slots_term=10
    )

    package1.save()
    package2.save()
    package3.save()
    return [package1, package2, package3]


@pytest.fixture
def vendorSubscription(vendor, subscriptionPackages):
    subcription = subsPriceModel.VendorSubscription(
        vendor=vendor,
        start_date='2021-09-01',
        end_date='2021-08-31',
        subscription=subscriptionPackages[0],
        total_amount_paid=120,
        applied_tax_rate=10,
        cycle_type='YEARLY',
        status='CURRENT'
    )
    subcription.save()
    return subcription


@pytest.fixture
def coupon(country, subscriptionPackages):
    coupon = revenueModel.Coupons(
        coupon_code='COUPON1',
        discountType='percent',
        discount_value=5,
        country=country,
        from_date='2021-09-12',
        to_date='2021-09-15',
        max_number_of_coupon=10
    )

    coupon.save()
    coupon.subscriptions.add(subscriptionPackages[0])
    coupon.subscriptions.add(subscriptionPackages[1])
    coupon.subscriptions.add(subscriptionPackages[2])
    coupon.save()
    return coupon
