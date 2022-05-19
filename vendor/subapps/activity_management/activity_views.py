from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers_activity as serializers
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator

from django.utils.decorators import method_decorator
from superadmin import decorators
from superadmin.subapps.media_and_groupings.models import AgeGroup
from superadmin.subapps.vendor_and_user_management.models import Vendor
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
    # permission_classes = (IsAuthenticated,)

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
    # permission_classes = (IsAuthenticated,)

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
    # permission_classes = (IsAuthenticated,)


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



class activeStatusView(APIView):

    def get(self,request):
            resultlist=[]
            # data=json.loads(request.body.decode('utf-8'))
            # vendor_status = ["vendor_status"]
            posts=Vendor.objects.filter(vendor_status="ACTIVE")
            print("llll",posts)

            
          
            if posts :
                for project in posts:
                    data = {
                    "vendor_name":project.name,
                    "vendor_code":project.vendor_code,
                    "activity_code":"100",
                    "activity_title": "swimming",
                    "Country": "usa",
                    "scheduled_classes": "1437",
                    "scheduled_session": "4561",
                    "activity_type": "Fixed timing",
                    "status":project.vendor_status,
                    }
                    resultlist.append(data)
            
                return JsonResponse({'data' : resultlist},status=status.HTTP_200_OK)
            else:
                return JsonResponse({'data' : resultlist},status=status.HTTP_400_BAD_REQUEST)        


class suspendedStatusView(APIView):

    def get(self,request):
            resultlist=[]
            # data=json.loads(request.body.decode('utf-8'))
            # vendor_status = ["vendor_status"]
            posts=Vendor.objects.filter(vendor_status="SUSPENDED")
            print("llll",posts)

            
          
            if posts :
                for project in posts:
                    data = {
                    "vendor_name":project.name,
                    "vendor_code":project.vendor_code,
                    "activity_code":"100",
                    "activity_title": "swimming",
                    "Country": "usa",
                    "scheduled_classes": "1437",
                    "scheduled_session": "4561",
                    "activity_type": "Fixed timing",  
                    "status":project.vendor_status,
                    }
                    resultlist.append(data)
            
                return JsonResponse({'data' : resultlist},status=status.HTTP_200_OK)
            else:
                return JsonResponse({'data' : resultlist},status=status.HTTP_400_BAD_REQUEST)        






# class activitytypeView(APIView):
#     serializer_class = serializers.activitytypeSerializer

#     @csrf_exempt
#     def post(self,request):
#         resultlist=[]
#         print("hello")
#         data=json.loads(request.body.decode('utf-8'))
#         start_date=data["start_date"]
#         print("start",start_date)
#         end_date=data["end_date"]
#         print(end_date)
#         check=data["check"]
#         print("check",check)
#         search_fields = data["vendor_name"]
#         search_fields1 = data["vendor_code"]
#         country_field=data["country_field"]
#         print("country",country_field)
#         if country_field == "":
#             country_field=0
            
#         z=Country.objects.filter(id = country_field).values_list("name",flat=True)
#         country=z[0]
#         print(data)
#         print("a",request.user.id)
#         post=Activity.objects.filter(name=search_fields).select_related("updated_by")
#         for i in post:
#             print(i.code)
#         #           
#         # post=Activity.objects.filter(=request.user.id)
#         if search_fields and search_fields1 and country_field:
#             posts=Activity.objects.filter(Q(name=search_fields),Q(country=country_field),Q(vendor_code=search_fields1),Q(vendor_code=search_fields1))
#             if posts :
#                 for project in posts:
#                     data = {
#                     "vendor_name":project.name,
#                     "vendor_code":project.vendor_code,
#                     "country":country,
#                     "status":project.vendor_status,
#                     }
#                     resultlist.append(data)
            
#                 return JsonResponse({'success': 'true','data' : resultlist})
#             else:
#                 return JsonResponse({'message': 'False','data' : resultlist})
#         elif search_fields and search_fields1:
#             posts1=Vendor.objects.filter(Q(name=search_fields),Q(vendor_code=search_fields1))
#             if posts1 :
#                 for project in posts1:
#                     data = {
#                     "vendor_name":project.name,
#                     "vendor_code":project.vendor_code,
#                     "country":country,
#                     "status":project.vendor_status,
#                     }
#                     resultlist.append(data)
            
#                 return JsonResponse({'success': 'true','data' : resultlist})
#             else:
#                 return JsonResponse({'message': 'False','data' : resultlist})
#         elif search_fields and country_field:    
#             posts2=Vendor.objects.filter(Q(name=search_fields),Q(country=country_field))
#             if posts2 :
#                 for project in posts2:
#                     data = {
#                     "vendor_name":project.name,
#                     "vendor_code":project.vendor_code,
#                     "country":country,
#                     "status":project.vendor_status,
#                     }
#                     resultlist.append(data)
            
#                 return JsonResponse({'success': 'true','data' : resultlist})
#             else:
#                 return JsonResponse({'message': 'False','data' : resultlist}) 
          
#         elif search_fields1 and country_field:   
#             posts3=Vendor.objects.filter(Q(vendor_code=search_fields1),Q(country=country_field))
#             if posts3 :
#                 for project in posts3:
#                     data = {
#                     "vendor_name":project.name,
#                     "vendor_code":project.vendor_code,
#                     "country":country,
#                     "status":project.vendor_status,
#                     }
#                     resultlist.append(data)
            
#                 return JsonResponse({'success': 'true','data' : resultlist})
#             else:
#                 return JsonResponse({'message': 'False','data' : resultlist})                



# class activitytypeView(APIView):
#     serializer_class = serializers.activitytypeSerializer
    
   
#     @csrf_exempt
#     def post(self,request):
#         resultlist=[]
#         print("hello")
#         data=json.loads(request.body.decode('utf-8'))
#         start_date=data["start_date"]
#         print("start",start_date)
#         end_date=data["end_date"]
#         print(end_date)
#         check=data["check"]
#         print("check",check)
#         vendor_name = data["vendor_name"]
#         print(type(vendor_name))
#         vendor_code = data["vendor_code"]
#         vendor_country=data["vendor_country"]
#         print("country",vendor_country)
#         if vendor_country == "":
#             vendor_country=0
      
#         w=Vendor.objects.filter(name=vendor_name).select_related('country')
#         for i in w:
#             print("ddmmm",i.country)  
#         z=Country.objects.filter(id = vendor_country).values_list("name",flat=True)
#         # country=z[0]
#         print(data)
#         print("a",request.user.id)
#         post=models.Activity.objects.filter(updated_by=1).select_related("vendor")
        
#         for i in post:
#             name_check=str(i.vendor)
#             print(type(name_check)) 
#             if  (str(vendor_name) == name_check):
#                 print("done")
#             status_check=str(i.vendor.vendor_status)
#         checkuser=models.Activity.objects.filter(updated_by=1).select_related("updated_by")
#         for i in post:
#             user_id=i.updated_by.id
#         mt=UserProfile.objects.filter(user=user_id)
#         for i in mt:
#             code_check=str(i.code)
#             print(code_check)
#             country_check=str(i.country.id)
#             country_name=str(i.country)
#             print(country_check)
#         if vendor_name and vendor_code and vendor_country:
#             print("innnn")
#             if vendor_name == name_check and vendor_code == code_check and vendor_country == country_check :
#                 print("in")
#                 data = {
#                 "vendor_name":name_check,
#                 "status":country_name,
#                  "vendor_code":code_check,
#                 "country_check":country_check,
#                 }
#                 resultlist.append(data)
#                 print("ss",resultlist)
        
#                 return JsonResponse({'success': 'true','data' : data})
#             else:
#                 return JsonResponse({'message': 'False','data' : resultlist})

#         elif vendor_name and vendor_country:
#             if vendor_name == name_check and  vendor_country == country_check :
#                 data = {
#                 "vendor_name":name_check,
#                 "vendor_code":code_check,
#                 "status":status_check,
#                 "country_check":country_check,
#                 }
#                 resultlist.append(data)
            
#                 return JsonResponse({'success': 'true','data' : data})
#             else:
#                 return JsonResponse({'message': 'False','data' : resultlist})