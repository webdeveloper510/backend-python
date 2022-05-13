from django.urls import path
from . import views

# for namespace. it is important to avoid name problems in {% url %}
app_name = 'static_info'

#Static Info URLs
urlpatterns = [
    path('staticinfo/<str:name>', views.StaticResourceList.as_view(), name='staticresourcelist'),
    path('staticContent/<int:id>', views.StaticContent.as_view(), name='staticContent'),
    path('logos', views.Logo.as_view(), name='logos'),
]
