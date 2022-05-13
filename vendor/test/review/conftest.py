# import pytest
# from vendor.subapps.activity_management import models as activity_models

# @pytest.fixture
# def activity(vendor, vendorUser):
#     return activity_models.Activity.objects.create(
#         title = 'title 1',
#         code = 'code1',
#         description = 'desc',
#         allowenrollment = True,
#         sessionenrollment = '',
#         teacherstudentratio = '1:10',
#         activitytype ='Day Access',
#         created_by = vendorUser,
#         noofsessions = 1,
#         count = '0',
#         registrationfee = 100,
#         isRegisterationFees = True,
#         materialfee = 0,
#         isMaterialFees = False,
#     )



# @pytest.fixture
# def review(user, activity):
#     return activity_models.Reviews.objects.create(
#         review='some random reviews',
#         ratings=5,
#         reviewed_by=user,
#         activity=activity
#     )
