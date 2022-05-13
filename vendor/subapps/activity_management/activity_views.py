from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers_activity as serializers
from . import models
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator

from django.utils.decorators import method_decorator
from superadmin import decorators
from superadmin.subapps.media_and_groupings.models import AgeGroup
from .serializers_categories import CategorySerializer
from .serializers_attributes import AttributeSerializer

class ActivityCreationAllowed(APIView):
    def get(self,request):
        types = list(dict(models.ACTIVITY_TYPES).keys())
        subscription = request.user.vendor_subscription

        term_activity = 'Term Activity'
        open_activity = 'Open Activity'
        fixed_activity = 'Fixed Time'
        day_access_activity = 'Day Access'

        if subscription.term_no_of_activities:
            activityCount = request.user.vendor_activities.filter(activitytype=term_activity).count()
            print(subscription.term_no_of_activities,activityCount)
            if activityCount >= subscription.term_no_of_activities:
                types.remove(term_activity)
        else:
            types.remove(term_activity)
        
        if subscription.open_no_of_activities:
            activityCount = request.user.vendor_activities.filter(activitytype=open_activity).count()
            if activityCount >= subscription.open_no_of_activities:
                types.remove(open_activity)
        else:
            types.remove(open_activity)

        if subscription.day_access_no_of_activities:
            activityCount = request.user.vendor_activities.filter(activitytype=day_access_activity).count()
            if activityCount >= subscription.open_no_of_activities:
                types.remove(day_access_activity)
        else:
            types.remove(day_access_activity)
        
        if subscription.fixed_no_of_activities:
            activityCount = request.user.vendor_activities.filter(activitytype=fixed_activity).count()
            if activityCount >= subscription.open_no_of_activities:
                types.remove(fixed_activity)
        else:
            types.remove(fixed_activity)

        return Response({"allowed":len(types) != 0})


class ActivityDropdowns(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        res = {}
        types = list(dict(models.ACTIVITY_TYPES).keys())
        subscription = request.user.vendor_subscription

        term_activity = 'Term Activity'
        open_activity = 'Open Activity'
        fixed_activity = 'Fixed Time'
        day_access_activity = 'Day Access'

        if subscription.term_no_of_activities:
            activityCount = request.user.vendor_activities.filter(activitytype=term_activity).count()
            print(subscription.term_no_of_activities,activityCount)
            if activityCount >= subscription.term_no_of_activities:
                types.remove(term_activity)
        else:
            types.remove(term_activity)
        
        if subscription.open_no_of_activities:
            activityCount = request.user.vendor_activities.filter(activitytype=open_activity).count()
            if activityCount >= subscription.open_no_of_activities:
                types.remove(open_activity)
        else:
            types.remove(open_activity)

        if subscription.day_access_no_of_activities:
            activityCount = request.user.vendor_activities.filter(activitytype=day_access_activity).count()
            if activityCount >= subscription.open_no_of_activities:
                types.remove(day_access_activity)
        else:
            types.remove(day_access_activity)
        
        if subscription.fixed_no_of_activities:
            activityCount = request.user.vendor_activities.filter(activitytype=fixed_activity).count()
            if activityCount >= subscription.open_no_of_activities:
                types.remove(fixed_activity)
        else:
            types.remove(fixed_activity)

        res["ActivityTypes"] = types

        max_sessions = {}
        
        for type in types:
            if type == term_activity:
                max_sessions[term_activity] = subscription.term_sessions_per_term
            elif type == open_activity:
                max_sessions[open_activity] = subscription.open_sessions_per_term
        res["max_sessions"] = max_sessions

        res['age_groups'] = request.user.userdetails.country.agegroups.values('name')

        categories = models.Category.objects.all()
        res['categories'] = CategorySerializer(categories,many=True).data

        attributes = models.Attribute.objects.all()
        res['attributes'] = AttributeSerializer(attributes,many=True).data
 
        return Response(res)

class Activities (APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = serializers.ActivitySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @method_decorator(decorators.log_db_read_operation)
    def get(self, request):
        obj = request.user.vendor_activities.all()
        if CustomLimitOffsetPaginator.limit_query_param in request.GET:
            paginator = CustomLimitOffsetPaginator()
            data = paginator.paginate_queryset(obj,request=request,view=self)

            serializer = serializers.ActivitySerializers(data, many=True)

            return paginator.get_paginated_response(serializer.data)
        
        return Response(serializers.ActivitySerializers(obj,many=True).data)
        
        

class Activity (APIView):
    permission_classes = (IsAuthenticated,)


    def put(self, request, id):
        try:
            obj = request.user.vendor_activities.get(id=id)
        except models.Activity.DoesNotExist:
            return Response({"error":"Activity not found."},status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ActivitySerializers(obj, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        try:
            obj = request.user.vendor_activities.get(id=id)
        except models.Activity.DoesNotExist:
            return Response({"error":"Activity not found."},status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ActivitySerializers(obj)
        return Response(serializer.data)