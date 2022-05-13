from django.urls import path
from . import views

# for namespace. it is important to avoid name problems in {% url %}
app_name = 'settings'

# User URLs
urlpatterns = [
    # For Superadmin
    path('userfeedback', views.SuperadminUserFeedback.as_view(), name='SuperadminUserFeedback'),

    # For Web and Mobile
    # for currently logged-in user
    path('users/invited', views.RegisterInvitedUser.as_view(), name='RegisterInvitedUser'),
    path('users/cancel/invitation/<int:id>', views.CancelInvitationOfUser.as_view(), name='RegisterInvitedUser'),

    path('user/feedback', views.CurrentUserFeedback.as_view(), name='CurrentUserFeedback'),
    
    path('user/family/add_admin', views.AddAdmin.as_view(), name='add_admin'),
    path('invitations/register/<str:token>', views.InvitationLandingPage.as_view(), name='InvitationLandingPage'),
]
