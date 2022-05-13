from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator
from superadmin.subapps.countries_and_cities.models import Country
from superadmin.subapps.vendor_and_user_management.models import Vendor
from vendor.subapps.activity_management import models as activity_management
from vendor.subapps.perticipants import models as perticipant_models
from . import serializers as perticipants_serializer
from vendor.subapps.profile.models import VendorLocation


class PerticipantsSerach(APIView):

    def get(self, request):
        all_perticipants = perticipant_models.Perticipants.objects.all()

        if "first_name" in request.query_params:

            firstName = request.query_params['first_name']
            all_perticipants = all_perticipants.filter(
                participant__first_name=firstName)
        if "last_name" in request.query_params:

            lastName = request.query_params['last_name']
            all_perticipants = all_perticipants.filter(
                participant__last_name=lastName)
        if "user_id" in request.query_params:
            user_id = request.query_params['user_id']
            all_perticipants = all_perticipants.filter(
                participant__userdetails__code=user_id)

        if 'city' in request.query_params:
            city = request.query_params['city']
            all_perticipants = all_perticipants.filter(
                location__city__name=city)

        paginator = CustomLimitOffsetPaginator()

        page = paginator.paginate_queryset(
            all_perticipants, request, view=self)
        serializer = perticipants_serializer.PerticipantsSerializer(
            page, many=True)
        if page is not None:
            return paginator.get_paginated_response(serializer.data)


class PerticipantsOfActivity(APIView):

    def get(self, request):
        errors = []
        # Search params are = [country, vendor code, vendor name, activity title, activity code, class id, session id]
        # response = [date, location, activity title, activity code, time, session id, name, user id, booking reference no]
        #
        if 'country' in request.query_params:
            country = request.query_params['country']

        else:
            error_obj = {'country': 'This params is required'}
            errors.append(error_obj)

        if 'vendor_code' in request.query_params:
            vendor_code = request.query_params['vendor_code']

        else:
            error_obj = {'vendor_code': 'This params is required'}
            errors.append(error_obj)

        if 'activity_code' in request.query_params:
            activity_code = request.query_params['activity_code']
        else:
            error_obj = {'activity_code': 'This params is required'}
            errors.append(error_obj)

        if 'location' in request.query_params:
            location = request.query_params['location']
        else:
            error_obj = {'location': 'This params is required'}
            errors.append(error_obj)

        if len(errors) > 0:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            country = Country.objects.get(name=country)
        except:
            return Response({'country': "Can't find any country with provided name."}, status=status.HTTP_404_NOT_FOUND)

        try:
            vendor = Vendor.objects.get(vendor_code=vendor_code)
        except:
            return Response({'vendor_code': "Can't find any vendor with provided vendor code."}, status=status.HTTP_404_NOT_FOUND)

        try:
            activity = activity_management.Activity.objects.get(
                code=activity_code)
        except:
            return Response({'activity_code': "Can't find any activity with provided activity code."}, status=status.HTTP_404_NOT_FOUND)

        try:
            location_obj = VendorLocation.objects.get(id=location)
        except:
            return Response({'location': "Can't find any location"}, status=status.HTTP_404_NOT_FOUND)

        results = []
        if activity.activitytype == 'Day Access':
            sessions_list = activity_management.Slot.objects.filter(
                activity=activity, location=location_obj)
            print(sessions_list)

            session_id = request.query_params.get('session_id', None)
            if session_id:
                sessions_list = sessions_list.filter(session_id=session_id)
            print(sessions_list)
            for session in sessions_list:
                obj = {
                    'date': session.slotdate,
                    'session_id': session.session_id,
                    'location': location_obj.address,
                    'activity_code': activity.code,
                    'activity_title': activity.title,
                    'total_perticipants': session.totalenrolled
                }
                serializer = perticipants_serializer.DayAccessSerializer(
                    session.dayParticipants.all(), many=True)
                obj['perticepants'] = serializer.data

                results.append(obj)

            return Response(results)

        if activity.activitytype == 'Fixed Term':
            sessions_list = activity_management.Fixedtimingslot.objects.filter(
                activity=activity, location=location_obj)
            session_id = request.query_params.get('session_id', None)
            if session_id:
                sessions_list = sessions_list.filter(session_id=session_id)
            for session in sessions_list:
                obj = {
                    'date': session.slotdate,
                    'session_id': session.session_id,
                    'location': location_obj.address,
                    'activity_code': activity.code,
                    'activity_title': activity.title,
                    'total_perticipants': session.totalenrolled
                }
                serializer = perticipants_serializer.DayAccessSerializer(
                    session.ftparticipants.all(), many=True)

                obj['perticepants'] = serializer.data

                results.append(obj)
            return Response(results)

        if activity.activitytype == 'Term activity':
            class_list = activity_management.TermActivity.objects.filter(
                activity=activity, location=location_obj)
            class_id = request.query_params.get('class_id', None)
            if class_id:
                class_list = class_list.filter(classid=class_id)
            main_obj = {'activity_code': activity.code,
                        'activity_title': activity.title, 'location': location_obj.address}
            for class_obj in class_list:
                sessions_list = class_obj.term_slot.all().values_list(
                    'slotdate', flat=True).distinct()
                session_id = request.query_params.get('session_id', None)
                if session_id:
                    sessions_list = sessions_list.filter(sessionid=session_id)
                for session in sessions_list:
                    obj = {
                        'date': session,
                    }
                    sessions = activity_management.TermActivitySlot.objects.filter(
                        slotdate=session)
                    serializer = perticipants_serializer.TermSerializerForPerticipants(
                        sessions, many=True)
                    obj['sessions'] = serializer.data

                    results.append(obj)
            main_obj['results'] = results
            return Response(main_obj)
        return Response({'message': 'All params are passed'})
