from django.urls import path
from . import views
# for namespace. it is important to avoid name problems in {% url %} and reverse
from .views import GoogleSocialAuthView, FacebookSocialAuthView

app_name = 'social_auth'


urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view()),
    path('facebook/', FacebookSocialAuthView.as_view()),
]
