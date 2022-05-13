from django.db.models import Q
from rest_framework import status, permissions
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response

from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator
from superadmin.subapps.vendor_and_user_management.models import Family
from superadmin.subapps.vendor_and_user_management.serializers import FamilySerializer

from .models import Perticipants, EvaluationList
from . import serializers as perticipant_serializer
from vendor.subapps.activity_management import models as activity_model
from vendor.subapps.profile.models import VendorLocation


class PerticipantsView(APIView):
    permissions = [permissions.IsAuthenticated]

    def get(self, request):
        # 1. Get all locations of a vendor
        locations = request.user.vendor.locations.all()
        # 2. finding perticipants with that locations in perticipants model
        perticipants = Perticipants.objects.filter(location__in=locations)
        # 3. ----- filter upcoming activity / class / sessions(How ???) ----
        # 4. filter the perticipants with first name
        if "first_name" in request.query_params:

            firstName = request.query_params['first_name']
            perticipants = perticipants.filter(
                participant__first_name=firstName)
        # 5. filter the perticipants with last name
        if "last_name" in request.query_params:

            lastName = request.query_params['last_name']
            perticipants = perticipants.filter(participant__last_name=lastName)
        # 6. filter the perticipants with user_id
        if "user_id" in request.query_params:
            user_id = request.query_params['user_id']
            perticipants = perticipants.filter(
                participant__userdetails__code=user_id)
        users_id = perticipants.values_list(
            'participant', flat=True).distinct()
        users = User.objects.filter(id__in=users_id)
        # serializer = perticipant_serializer.PerticipantListForVendor(
        #     users, many=True)
        paginator = CustomLimitOffsetPaginator()

        page = paginator.paginate_queryset(users, request, view=self)
        serializer = perticipant_serializer.PerticipantListForVendor(
            page, many=True)
        if page is not None:
            return paginator.get_paginated_response(serializer.data)
        # return Response(serializer.data, status=status.HTTP_200_OK)


class FindParticipentOfAActivityInFeature(APIView):

    permission_class = [permissions.IsAuthenticated]

    def get(self, request):
        title = request.query_params.get('title')
        code = request.query_params.get('code')
        location = request.query_params.get('location', None)
        if not title and not code:
            return Response({'success': False, 'message': 'Title or Code need to provided'}, status=status.HTTP_400_BAD_REQUEST)
        if location is None:
            return Response({'success': False, 'message': 'Location need to be provide'}, status=status.HTTP_400_BAD_REQUEST)
        if title:
            try:
                activity = activity_model.Activity.objects.get(title=title)
            except activity_model.Activity.DoesNotExist:
                return Response({'success': False, 'message': "Activity can't found with this title"}, status=status.HTTP_404_NOT_FOUND)
        if code:
            try:
                activity = activity_model.Activity.objects.get(code=code)
            except activity_model.Activity.DoesNotExist:
                return Response({'success': False, 'message': "Activity can't found with this code"}, status=status.HTTP_404_NOT_FOUND)
        try:
            location_obj = VendorLocation.objects.get(
                id=location, vendor=request.user.vendor)
        except VendorLocation.DoesNotExist:
            return Response({'location': 'Location does not find'}, status=status.HTTP_404_NOT_FOUND)
        results = []
        if activity.activitytype == 'Day Access':
            sessions_list = activity_model.Slot.objects.filter(
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
                serializer = perticipant_serializer.DayAccessSerializer(
                    session.dayParticipants.all(), many=True)
                obj['perticepants'] = serializer.data

                results.append(obj)
            return Response(results)

        if activity.activitytype == 'Fixed Term':
            sessions_list = activity_model.Fixedtimingslot.objects.filter(
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
                serializer = perticipant_serializer.DayAccessSerializer(
                    session.ftparticipants.all(), many=True)

                obj['perticepants'] = serializer.data

                results.append(obj)
            return Response(results)

        if activity.activitytype == 'Term activity':
            class_list = activity_model.TermActivity.objects.filter(
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
                    sessions = activity_model.TermActivitySlot.objects.filter(
                        slotdate=session)
                    serializer = perticipant_serializer.TermSerializerForPerticipants(
                        sessions, many=True)
                    obj['sessions'] = serializer.data

                    results.append(obj)
            main_obj['results'] = results
            return Response(main_obj)


class FindParticipentOfAActivityInPast(APIView):

    permission_class = [permissions.IsAuthenticated]

    def get(self, request):
        title = request.query_params.get('title')
        code = request.query_params.get('code')
        location = request.query_params.get('location', None)
        if not title and not code:
            return Response({'success': False, 'message': 'Title or Code need to provided'}, status=status.HTTP_400_BAD_REQUEST)
        if location is None:
            return Response({'success': False, 'message': 'Location need to be provide'}, status=status.HTTP_400_BAD_REQUEST)
        if title:
            try:
                activity = activity_model.Activity.objects.get(title=title)
            except activity_model.Activity.DoesNotExist:
                return Response({'success': False, 'message': "Activity can't found with this title"}, status=status.HTTP_404_NOT_FOUND)
        if code:
            try:
                activity = activity_model.Activity.objects.get(code=code)
            except activity_model.Activity.DoesNotExist:
                return Response({'success': False, 'message': "Activity can't found with this code"}, status=status.HTTP_404_NOT_FOUND)
        try:
            location_obj = VendorLocation.objects.get(
                id=location, vendor=request.user.vendor)
        except VendorLocation.DoesNotExist:
            return Response({'location': 'Location does not find'}, status=status.HTTP_404_NOT_FOUND)
        results = []
        if activity.activitytype == 'Day Access':
            sessions_list = activity_model.Slot.objects.filter(
                activity=activity, location=location_obj)
            for session in sessions_list:
                obj = {
                    'date': session.slotdate,
                    'total_perticipants': session.totalenrolled
                }
                serializer = perticipant_serializer.DayAccessSerializer(
                    session.dayParticipants.all(), many=True)
                # serializer = perticipants_serializer.participantSerializer(
                #     session.enrolments.all(), many=True)
                obj['perticepants'] = serializer.data

                results.append(obj)
            return Response(results)

        if activity.activitytype == 'Fixed Term':
            sessions_list = activity_model.Fixedtimingslot.objects.filter(
                activity=activity, location=location_obj)
            for session in sessions_list:
                obj = {
                    'date': session.slotdate,
                    'total_perticipants': session.totalenrolled,
                    'hasEvaluation': activity.evaluation,
                    'hasCertification': True
                }
                serializer = perticipant_serializer.DayAccessForPastActivitySerializer(
                    session.ftparticipants.all(), many=True)
                # serializer = perticipants_serializer.participantSerializer(
                #     session.enrolments.all(), many=True)
                obj['perticepants'] = serializer.data
                if activity.evaluation:
                    evaluations = activity.activityAttr.all()
                    arr = []
                    for eval in evaluations:
                        act = EvaluationList.objects.filter(evaluation=eval)
                        eval_serializer = perticipant_serializer.EvaluationListSerializer(
                            act, many=True)
                        arr.append({eval.attribute.name: eval_serializer.data})
                    obj['evaluatins'] = arr

                results.append(obj)
            return Response(results)

        if activity.activitytype == 'Term activity':
            class_list = activity_model.TermActivity.objects.filter(
                activity=activity, location=location_obj)
            for class_obj in class_list:
                sessions_list = class_obj.term_slot.all().values_list(
                    'slotdate', flat=True).distinct()
                for session in sessions_list:
                    obj = {
                        'date': session,
                    }
                    sessions = activity_model.TermActivitySlot.objects.filter(
                        slotdate=session)
                    serializer = perticipant_serializer.TermSerializerForPerticipants(
                        sessions, many=True)
                    # serializer = perticipants_serializer.participantSerializer(
                    #     session.enrolments.all(), many=True)
                    obj['sessions'] = serializer.data

                    results.append(obj)
            return Response(results)


class PertcipantsCertificatViews(APIView):
    permission_class = [permissions.IsAuthenticated]

    def get(self, request, pert_id):
        perticepent = Perticipants.objects.get(id=pert_id)
        serializer = perticipant_serializer.DayAccessForPastActivitySerializer(
            perticepent)

        return Response(serializer.data)

    def post(self, request, pert_id):
        # try:
        perticepent = Perticipants.objects.get(id=pert_id)
        # TODO: check if the activity is Day access activity
        if perticepent.activity.activitytype == "Day Access":
            return Response({'success': False, 'message': 'Day acess type of activity has not certification.'}, status=status.HTTP_400_BAD_REQUEST)
        # TODO: If the activity is not Day access,  has certification permission

        serializer = perticipant_serializer.DayAccessForPastActivitySerializer(
            perticepent, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        # except Exception as e:
        #     print(e)
        #     return Response({'success': False, 'message': "Perticepent doesn't found"}, status=status.HTTP_404_NOT_FOUND)


class SearchClassDetails(APIView):
    permission_class = [permissions.IsAuthenticated]

    def get(self, request):
        # TODO: when Open activity will be ready
        results = []
        title = request.query_params.get('title')
        code = request.query_params.get('code')
        location = request.query_params.get('location', None)
        if not title and not code:
            return Response({'success': False, 'message': 'Title or Code need to provided'}, status=status.HTTP_400_BAD_REQUEST)
        if location is None:
            return Response({'success': False, 'message': 'Location need to be provide'}, status=status.HTTP_400_BAD_REQUEST)
        if title:
            try:
                activity = activity_model.Activity.objects.get(title=title)
            except activity_model.Activity.DoesNotExist:
                return Response({'success': False, 'message': "Activity can't found with this title"}, status=status.HTTP_404_NOT_FOUND)
        if code:
            try:
                activity = activity_model.Activity.objects.get(code=code)
            except activity_model.Activity.DoesNotExist:
                return Response({'success': False, 'message': "Activity can't found with this code"}, status=status.HTTP_404_NOT_FOUND)
        try:
            location_obj = VendorLocation.objects.get(
                id=location, vendor=request.user.vendor)
        except VendorLocation.DoesNotExist:
            return Response({'location': 'Location does not find'}, status=status.HTTP_404_NOT_FOUND)

        class_id = request.query_params.get('class_id')
        if activity.activitytype == 'Term activity':
            return_obj = {
                'activity_title': activity.title,
                'activity_code': activity.code,
                'class_id': class_id,
                'location': location_obj.address
            }

            class_id = request.query_params.get('class_id', None)
            try:
                class_obj = activity_model.TermActivity.objects.get(
                    activity=activity, location=location_obj, classid=class_id)
            except activity_model.TermActivity.DoesNotExist as e:
                return Response({'class_id': "Doesn't find this class id"}, status=status.HTTP_404_NOT_FOUND)

            sessions_list = class_obj.term_slot.all()

            session_serializer = perticipant_serializer.SessionsSerializer(
                sessions_list, many=True)
            return_obj['sessions'] = session_serializer.data
            perticipants = Perticipants.objects.filter(
                term_activityslot=class_obj)
            perticipantSerialzier = perticipant_serializer.DayAccessSerializer(
                perticipants, many=True)

            return_obj['perticipants'] = perticipantSerialzier.data

            return Response(return_obj)
        else:
            return Response({'error': True, 'message': 'Open activity is in building'}, status=status.HTTP_400_BAD_REQUEST)


class Evaluations(APIView):
    permission_class = [permissions.IsAuthenticated]

    def post(self, request):
        resp_arr = []
        try:
            evaluation_data = request.data['evaluation_data']
        except:
            return Response({'evaluation_data': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            for item in evaluation_data:
                perticipant_id = item.get('perticipant_id', None)
                if perticipant_id:
                    try:
                        pertcipant = Perticipants.objects.get(
                            id=perticipant_id)
                        pertcipant.evperticipants.all().delete()
                    except Perticipants.DoesNotExist:
                        return Response({'perticipant_id': f"{perticipant_id} does not found"}, status=status.HTTP_404_NOT_FOUND)

                    evaluations = item.get('evaluations')
                    try:
                        assert type(
                            evaluations) == list, ('evaluations must be in dict/array')
                    except AssertionError:
                        return Response({'error': True, 'evaluations': ('evaluations must be in dict')}, status=status.HTTP_400_BAD_REQUEST)

                    for eval in evaluations:
                        eval['perticipant'] = perticipant_id
                        serializer = perticipant_serializer.EvaluationListSerializer(
                            data=eval)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        resp_arr.append(serializer.data)
                else:
                    return Response({'perticipant_id': "This field is required"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(resp_arr, status=status.HTTP_200_OK)


class EnrollmentUsers(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):

        activities = activity_model.Activity.objects.filter(created_by=request.user)
        # check enrolment with this activities
        enrolments = Perticipants.objects.filter(
            activity__in=activities)
        # from activities check in family
        lists = []
        for enrolment in enrolments:

            enroled_by = enrolment.enrolled_by
            try:
                family = Family.objects.get(Q(
                    superadmin=enroled_by
                ) | Q(
                    admin=enroled_by
                ))
            except:
                family = Family(superadmin=enroled_by)
                family.save()
            family_members = [kid.user for kid in family.kids.all()]
            family_members.append(family.superadmin)
            if family.admin:
                family_members.append(family.admin)
            family_enrolled = enrolments.filter(participant__in=family_members)

            if(len(family_enrolled)):
                # past_enrolments = [data['sessions'] for data in family_enrolled.filter(
                #     status='PAST').values('sessions').distinct()]
                # past_list = []
                # for session in past_enrolments:
                #     past_list.append(Perticipants.objects.filter(
                #         sessions=session).first())
                # family_enrolled = [data['sessions'] for data in family_enrolled.exclude(
                #     id__in=past_enrolments).values('sessions').distinct()]
                # ongoing_list = []
                # for session in family_enrolled:
                #     ongoing_list.append(Perticipants.objects.filter(
                #         sessions=session).first())
                serializer = perticipant_serializer.FamilySerializer(family)
                enrol_serializer = perticipant_serializer.EnrolmentsSerialzer(
                    family_enrolled, many=True)

                past_enrol_serializer = perticipant_serializer.EnrolmentsSerialzer(
                    family_enrolled, many=True)
                obj = serializer.data
                obj['ongoing_or_upcoming'] = {
                    "count": len(family_enrolled),
                    "activities": enrol_serializer.data
                }
                obj['past'] = {
                    "count": len(family_enrolled),
                    "activities": past_enrol_serializer.data
                }
                lists.append(obj)

        paginator = CustomLimitOffsetPaginator()
        # if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, 1)):
        page = paginator.paginate_queryset(lists, request, view=self)

        if page is not None:
            return paginator.get_paginated_response(lists)
        # return Response({'data': lists})
