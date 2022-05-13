from django.urls import path
from . import views


app_name = 'perticipants'

urlpatterns = [
    path('participants', views.PerticipantsView.as_view(),
         name='vendor_participants'),
    path('search-activity/perticipants',
         views.FindParticipentOfAActivityInFeature.as_view(), name="findPerticipants"),
    path('search/class_id/', views.SearchClassDetails.as_view(), name='SearchClass'),
    path('search-past-activity/perticipants',
         views.FindParticipentOfAActivityInPast.as_view(), name="findPerticipants"),
    path('perticipant/certificate/<int:pert_id>/',
         views.PertcipantsCertificatViews.as_view(), name='perticepent_certificate'),
    path('perticipant/add-evaluation/',
         views.Evaluations.as_view(), name='evaluationAdd'), 
    path('vendor/users', views.EnrollmentUsers.as_view(),
         name='vendorUsers')
]
