from django.urls import path
from . import views
app_name = 'perticipants'

urlpatterns = [
    path('search-perticipants/', views.PerticipantsSerach.as_view(),
         name='search_perticipants'),
    path('search-activity/perticipents', views.PerticipantsOfActivity.as_view(),
         name='search_activity_perticipents')
]
