from django.urls import path
from . import activity_views as views
from . import views_slots
from . import views_fixedtiming_slots as views_fixedtiming
from . import views_attributes as view_attributes
from . import views_reviews
from . import views_termactivity
from . import views_categories
from . import activity_views

# for namespace. it is important to avoid name problems in {% url %}
app_name = 'activity_management'

# Countries & Cities URLs
urlpatterns = [
    # Unsecured endpoints
    path('activity/dropdowns', views.ActivityDropdowns.as_view(),name='activityTypes'),
    path('activityCreationAllowed', views.ActivityCreationAllowed.as_view(),name='activityTypes'),
    path('activities', views.Activities.as_view(),name='activities'),  # Open (Unsecured) Endpoint
    path('activity/<int:id>', views.Activity.as_view(), name='activity'),
    path('activity/<int:id>/slots', views_slots.Slots.as_view(), name='slots'),
    path('activity/fixedtiming/all', views_fixedtiming.FixedSlotsListView.as_view()),
    path('activity/fixedtiming/<int:pk>', views_fixedtiming.FixedSlotsDetailsView.as_view()),
    path('activity/fixedtimingday/all', views_fixedtiming.TimeSlotListView.as_view()),
    path('activity/fixedtimingday/<int:pk>', views_fixedtiming.TimeSlotDetailsView.as_view()),
    path('activity/termactivity/all', views_termactivity.TermActivityListView.as_view()),
    path('activity/termactivity/<int:pk>', views_termactivity.TermActivityDetailsView.as_view()),
    path('activity/termactivityslot/all', views_termactivity.TermActivitySlotListView.as_view()),
    path('activity/termactivityslot/<int:pk>', views_termactivity.TermActivitySlotDetailsView.as_view()),
    path('attributes/all', view_attributes.AttributeListView.as_view()),
    path('attributes/<int:pk>', view_attributes.AttributeDetailsView.as_view()),
    path('attributes/<int:pk>/subattributes', view_attributes.SubAttributesView.as_view()),
    path('categories/all', views_categories.CategoryListView.as_view()),
    path('categories/<int:pk>', views_categories.CategoryDetailsView.as_view()),
    path('categories/<int:pk>/subcategories', views_categories.SubCategoriesView.as_view()),
    path('categories/UpdateCategoryWeightages', views_categories.UpdateCategoryWeightageView.as_view()),

  #api for status
    path('activeStatusView', activity_views.activeStatusView.as_view(), name='activeStatusView'),
    path('suspendedStatusView', activity_views.suspendedStatusView.as_view(), name='suspendedStatusView'),
   
]


# Reviews Urls
urlpatterns += [
    path('reviews', views_reviews.Reviews.as_view(), name='reviews'),
    path('reviews/<int:id>', views_reviews.Review.as_view(), name='review'),
    path('vendor-reviews', views_reviews.VendorReviews.as_view(),
         name='vendor_reviews'),
    path('vendor-review/<int:id>', views_reviews.VendorReview.as_view(),
         name='vendor_review'),
]
