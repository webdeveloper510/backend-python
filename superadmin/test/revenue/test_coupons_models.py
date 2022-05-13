import pytest
from superadmin.subapps.revenue import models as revenueModel


@pytest.mark.django_db
def test_CouponModel(country, subscriptionPackages, vendorSubscription):
    coupon = revenueModel.Coupons(
        coupon_code='COUPON1',
        discountType='percent',
        discount_value=100,
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

    coupons = revenueModel.Coupons.objects.all()
    assert len(coupons) == 1
    assert len(coupons[0].subscriptions.all()) == 3
    assert coupons[0].coupon_code == coupon.coupon_code

    couponDetails = revenueModel.couponRedemptionDetails(
        vendorSubscription=vendorSubscription,
        coupon = coupons[0]
    )

    couponDetails.save()
    assert len(revenueModel.couponRedemptionDetails.objects.all()) == 1
    




# pytest test_coupons_models.py -s
