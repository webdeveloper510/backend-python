from functools import partial
from rest_framework import serializers, status, permissions,  generics
from rest_framework.response import Response
from rest_framework.views import APIView


from vendor.subapps.perticipants import models as pt_model
from .trialPerticipantsSerializer import TrialClassSerializer
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator


class TrialPerticipantsViews(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomLimitOffsetPaginator
    serializer_class = TrialClassSerializer

    def get_queryset(self):
        my_loc = self.request.user.vendor.locations.all()
        trial_class = pt_model.Perticipants.objects.filter(location__in=my_loc)
        if 'status' in self.request.query_params:
            status = self.request.query_params['status']
            trial_class = trial_class.filter(status=status)

        return trial_class


class TrialPerticipantViews(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomLimitOffsetPaginator
    serializer_class = TrialClassSerializer

    def get_queryset(self):
        my_loc = self.request.user.vendor.locations.all()
        trial_class = pt_model.Perticipants.objects.filter(location__in=my_loc)
        if 'status' in self.request.query_params:
            status = self.request.query_params['status']
            trial_class = trial_class.filter(status=status)

        return trial_class

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request,  *args, **kwargs)


class ChangeStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, status_name):
        try:
            pert = pt_model.Perticipants.objects.get(id=id)

        except:
            return Response({'success': False, 'message': 'Perticipants does not found'}, status=status.HTTP_404_NOT_FOUND)
        current_status = pert.status

        if current_status == 'ACTIVE':
            return Response({'success': False, 'status': 'Sorry, right now activity is active so there can not happen any status change.'}, status=status.HTTP_400_BAD_REQUEST)

        if current_status == 'EXPIRED':
            return Response({'success': False, 'status': 'Activity is already expired. So there can not happen any status change.'}, status=status.HTTP_400_BAD_REQUEST)

        if status_name in dict(pt_model.MARKETING_STATUS).keys():

            if current_status == 'SCHEDULED':
                if status_name == 'SUSPENDED':
                    pert.status = status_name
                    pert.save()
                    serializer = TrialClassSerializer(pert)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'success': False, 'message': 'Only you can suspend the perticipant'}, status=status.HTTP_400_BAD_REQUEST)

            elif current_status == 'SUSPENDED':
                if status_name == 'SCHEDULED' and pert.start_date():
                    pert.status = status_name
                    pert.save()
                    serializer = TrialClassSerializer(pert)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'success': False, 'message': 'Activity is expired or continuing. So you can not reinstate it.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success': False, 'status': 'This is not a valid status'}, status=status.HTTP_400_BAD_REQUEST)
