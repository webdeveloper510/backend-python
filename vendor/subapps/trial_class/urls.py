from django.urls import path
from . import views as tc


app_name = 'trial_class'

urlpatterns = [
    path('trialclass/perticipatns',
         tc.TrialPerticipantsViews.as_view(), name='trial_perticipant'),
         
    path('trialclass/perticipatns/<int:pk>',
         tc.TrialPerticipantViews.as_view(), name='trial_perticipant_update'),

    path('trialclass/perticipatns/<int:id>/<str:status_name>/',
         tc.ChangeStatus.as_view(), name='change_status')
]
