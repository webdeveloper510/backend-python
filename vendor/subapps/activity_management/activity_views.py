from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers_activity as serializers
from . import models
from authentication.models import UserProfile ,User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator

from django.utils.decorators import method_decorator
from superadmin import decorators
from .serializers_activity import activityStatusSerializer
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
            posts=Vendor.objects.filter(vendor_status="ACTIVE")
            print("llll",posts)         
          
            if posts :
                for project in posts:
                    data = {
                    "vendor_name":project.name,
                    "vendor_code":project.vendor_code,
                    "activity_code":"100",
                    "activity_title": "swimming",
                    "country": "usa",
                    "scheduled_classes": "1437",
                    "scheduled_session": "4561",
                    "activity_type": "Fixed timing",
                    "status":project.vendor_status,
                    }
                    resultlist.append(data)
            
                return JsonResponse({'data' : resultlist},status=status.HTTP_200_OK)
            else:
                return JsonResponse({'data' : resultlist},status=status.HTTP_400_BAD_REQUEST)        
    



class vendorNameSuggestion(APIView):    
    def post(self,request):
        resultlist=[]
        data=json.loads(request.body.decode('utf-8'))
        vendor_name=data["vendor_name"]
        if vendor_name == "":
            return Response({"error":"Name not found."},status=status.HTTP_404_NOT_FOUND)        
        else:
            shipper = Vendor.objects.filter(Q(name__icontains=vendor_name))
            print("hfdsfnnfsknf",shipper)
            if shipper :
                    for project in shipper:
                        data = {
                        "vendor_name":project.name,
                        }
                        resultlist.append(data)
                
                    return JsonResponse({'data' : resultlist},status=status.HTTP_200_OK)
            else:
                return Response({"error":"Name not found."},status=status.HTTP_404_NOT_FOUND)        


        





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
                "country": "usa",
                "scheduled_classes": "1437",
                "scheduled_session": "4561",
                "activity_type": "Fixed timing",  
                "status":project.vendor_status,
                }
                resultlist.append(data)
        
            return JsonResponse({'data' : resultlist},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'data' : resultlist},status=status.HTTP_400_BAD_REQUEST)        









# class activitySearchView(APIView):  
    
    
#     def post(self,request):
        
#         resultlist = []
#         data=json.loads(request.body.decode('utf-8'))
#         searchdata = request.GET.get('data')
#         print("=============",searchdata)
#         vendor_search=data["vendor_search"]
        
#         shipper = Vendor.objects.filter(Q(name__icontains=vendor_search)|Q(vendor_code__icontains=vendor_search)|Q(email__icontains=vendor_search)|Q(status__icontains=vendor_search)|Q(vendor_status__icontains=vendor_search))
#         activity_obj = Activity.objects.filter(Q(code__icontains=vendor_search)|Q(vendor_code__icontains=vendor_search)|Q(email__icontains=vendor_search)|Q(status__icontains=vendor_search)|Q(vendor_status__icontains=vendor_search))
#         print(activity_obj)

#         print(shipper)

#         if shipper:
#             for project in shipper:
#                             data = {
#                             "name":project.name,
#                             "vendor_code":project.vendor_code,
#                             # "activity_code":project.activity_code,
#                             "email": project.email,
#                             "vendor_status": project.vendor_status,
#                             "created_at": project.created_at,
#                             # "country": project.country,
#                             # "scheduled_classes": project.scheduled_classes,
#                             # "scheduled_session": project.scheduled_session,
#                             # "activity_type": project.activity_type, 
#                             "status":project.status,
#                             "city_id":project.city_id,
#                             }
#                             resultlist.append(data)
#             return JsonResponse({'success': 'true','data' : resultlist})


#         else:
#             return JsonResponse({'message': 'False','data' : resultlist})








class activitySearchView(APIView):  
    
    
    def post(self,request):
        
        resultlist = []
        data=json.loads(request.body.decode('utf-8'))
        vendor_search=data["vendor_search"]
        if vendor_search == "":
            print("")
            return JsonResponse({'message': 'False','data' : resultlist})

        else:
            shipper = Vendor.objects.filter(Q(name__icontains=vendor_search)|Q(vendor_code__icontains=vendor_search)|Q(email__icontains=vendor_search)|Q(status__icontains=vendor_search)|Q(vendor_status__icontains=vendor_search))

            print(shipper)

            if shipper:
                for project in shipper:
                                data = {
                                "vendor_name":project.name,
                                "vendor_code":project.vendor_code,
                                "activity_title":'act_title',
                                "activity_code":'012',
                                "email": project.email,
                                "vendor_status": project.vendor_status,
                                "created_at": project.created_at,
                                "country": 'USA',
                                "scheduled_classes":'1200',
                                "scheduled_session": '4.100',
                                "activity_type": 'USA', 
                                "status":project.status,
                                }
                                resultlist.append(data)
                return JsonResponse({'success': 'true','data' : resultlist})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})






class activitytypeView(APIView):
    serializer_class = serializers.activitytypeSerializer
    
   
    @csrf_exempt
    def post(self,request):
        resultlist=[]
        print("hello")
        # user_obj=User.objects.get(id=user_id)
        # print("user_obj",user_obj.id)
        data=json.loads(request.body.decode('utf-8'))
        start_date=data["start_date"]
        print("start",start_date)
        end_date=data["end_date"]
        print(end_date)
        vendor_name = data["vendor_name"]
        print(type(vendor_name))
        vendor_code = data["vendor_code"]
        vendor_country=data["vendor_country"]
        print("country",vendor_country)
        if vendor_country == "":
            vendor_country=0
      
        w=Vendor.objects.filter(name=vendor_name).select_related('country')
        for i in w:
            print("ddmmm",i.country)  
        print("a",request.user.id)
        post=models.Activity.objects.filter(updated_by=1).select_related("vendor")
        post1=models.Activity.objects.filter(updated_by=1).values_list("activitytype",flat=True)
        post2=models.Activity.objects.filter(updated_by=1).values_list("title",flat=True)
        activitytitle=post2[0]
        post3=models.Activity.objects.filter(updated_by=1).values_list("code",flat=True)
        activitycode=post3[0]
        actitvitytype=post1[0]
        
        for i in post:
            name_check=str(i.vendor)
            print(type(name_check)) 
            if  (str(vendor_name) == name_check):
                print("done")
            status_check=str(i.vendor.vendor_status)
            id_vendor=str(i.vendor.vendor.id)
            print("qqqqqq",id_vendor)
        
            mt=UserProfile.objects.filter(user=id_vendor)
        for i in mt:
            code_check=str(i.code)
            print(code_check)
            country_check=str(i.country.id)
            country_name=str(i.country)
            print(country_check)
        if vendor_name and vendor_code and vendor_country and start_date and end_date:  
            if vendor_name == name_check and vendor_code == code_check and vendor_country == country_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                data = {
                "vendor_name":name_check,
                "status":status_check,
                 "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                 "scheduled_classes":"1000",
                "scheduled_session":"10000"
                }
                resultlist.append(data)
                print("ss",resultlist)
        
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
        
        elif vendor_name and vendor_code and start_date and end_date:  
            if vendor_name == name_check and vendor_code == code_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                data = {
                "vendor_name":name_check,
                "status":status_check,
                 "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                 "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                }
                resultlist.append(data)
                print("ss",resultlist)
        
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
        
        elif  vendor_country and vendor_code and start_date and end_date:  
            if vendor_country == country_check  and vendor_code == code_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                data = {
                "vendor_name":name_check,
                "status":status_check,
                 "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                 "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                }
                resultlist.append(data)
                print("ss",resultlist)
        
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
            
        elif  vendor_name and vendor_country and start_date and end_date:  
            if vendor_name == name_check  and  vendor_country == country_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                data = {
                "vendor_name":name_check,
                "status":status_check,
                 "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                 "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                }
                resultlist.append(data)
                print("ss",resultlist)
        
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
            
        elif vendor_name and  start_date and end_date:
            if vendor_name == name_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                data = {
                "vendor_name":name_check,
                "status":status_check,
                 "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                 "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                }
                resultlist.append(data)
                print("ss",resultlist)
        
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
            
        elif vendor_code and  start_date and end_date:
            if vendor_code == code_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                data = {
                "vendor_name":name_check,
                "status":status_check,
                 "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                 "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                }
                resultlist.append(data)
                print("ss",resultlist)
        
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})    
            
            
        elif vendor_country and  start_date and end_date:
            if vendor_country == country_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                data = {
                "vendor_name":name_check,
                "status":status_check,
                 "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                 "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                }
                resultlist.append(data)
                print("ss",resultlist)
        
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})        
            
        elif vendor_name and vendor_code and vendor_country:
            if vendor_name == name_check and vendor_code == code_check and vendor_country == country_check:
                data = {
                "vendor_name":name_check,
                "status":status_check,
                 "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                 "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                }
                resultlist.append(data)
                print("ss",resultlist)
        
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})

        elif vendor_name and vendor_country :
            if vendor_name == name_check and  vendor_country == country_check :
                data = {
                "vendor_name":name_check,
                "status":status_check,
                 "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                 "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                }
                resultlist.append(data)
            
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
        elif vendor_code and vendor_name:    
            if vendor_name == name_check and  vendor_code == code_check  :
                data = {
                "vendor_name":name_check,
                "status":status_check,
                 "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                 "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                }
                resultlist.append(data)
            
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
          
        elif vendor_code and vendor_country:   
            if vendor_country == country_check  and  vendor_code == code_check   :
                data = {
                "vendor_name":name_check,
                "status":status_check,
                 "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                 "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                }
                resultlist.append(data)
            
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
        else:
            if start_date == "" and end_date == "":
                start_date="3000-05-01"
                end_date="3000-05-01"
           
            if vendor_name == name_check or vendor_code == code_check or vendor_country == country_check or models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)) :
                data = {
                "vendor_name":name_check,
                "status":status_check,
                    "vendor_code":code_check,
                "country":country_name,
                "activity_type":actitvitytype,
                "activity_code":activitycode,
                "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                }
                resultlist.append(data)
                print("ss",resultlist)
    
                return JsonResponse({'success': 'true','data' : data})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})


        
class activityactiveView(APIView):
    serializer_class = serializers.activitytypeSerializer
    
   
    @csrf_exempt
    def post(self,request):
        resultlist=[]
        print("hello")
        # user_obj=User.objects.get(id=user_id)
        # print("user_obj",user_obj.id)
        data=json.loads(request.body.decode('utf-8'))
        start_date=data["start_date"]
        print("start",start_date)
        end_date=data["end_date"]
        print(end_date)
        vendor_name = data["vendor_name"]
        print(type(vendor_name))
        vendor_code = data["vendor_code"]
        vendor_country=data["vendor_country"]
        print("country",vendor_country)
        if vendor_country == "":
            vendor_country=0
      
        w=Vendor.objects.filter(name=vendor_name).select_related('country')
        for i in w:
            print("ddmmm",i.country)  
        print("a",request.user.id)
        post=models.Activity.objects.filter(updated_by=1).select_related("vendor")
        post1=models.Activity.objects.filter(updated_by=1).values_list("activitytype",flat=True)
        post2=models.Activity.objects.filter(updated_by=1).values_list("title",flat=True)
        activitytitle=post2[0]
        post3=models.Activity.objects.filter(updated_by=1).values_list("code",flat=True)
        activitycode=post3[0]
        actitvitytype=post1[0]
        
        for i in post:
            name_check=str(i.vendor)
            print(type(name_check)) 
            if  (str(vendor_name) == name_check):
                print("done")
            status_check=str(i.vendor.vendor_status)
            id_vendor=str(i.vendor.vendor.id)
            print("qqqqqq",id_vendor)
        
            mt=UserProfile.objects.filter(user=id_vendor)
        for i in mt:
            code_check=str(i.code)
            print(code_check)
            country_check=str(i.country.id)
            country_name=str(i.country)
            print(country_check)

        if Vendor.objects.filter(vendor_status="ACTIVE"):  
            if vendor_name and vendor_code and vendor_country and start_date and end_date:  
                if vendor_name == name_check and vendor_code == code_check and vendor_country == country_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
            
            elif vendor_name and vendor_code and start_date and end_date:  
                if vendor_name == name_check and vendor_code == code_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
            
            elif  vendor_country and vendor_code and start_date and end_date:  
                if vendor_country == country_check  and vendor_code == code_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
                
            elif  vendor_name and vendor_country and start_date and end_date:  
                if vendor_name == name_check  and  vendor_country == country_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
                
            elif vendor_name and  start_date and end_date:
                if vendor_name == name_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
                
            elif vendor_code and  start_date and end_date:
                if vendor_code == code_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})    
                
                
            elif vendor_country and  start_date and end_date:
                if vendor_country == country_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})        
                
            elif vendor_name and vendor_code and vendor_country:
                if vendor_name == name_check and vendor_code == code_check and vendor_country == country_check:
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})

            elif vendor_name and vendor_country :
                if vendor_name == name_check and  vendor_country == country_check :
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
            elif vendor_code and vendor_name:    
                if vendor_name == name_check and  vendor_code == code_check  :
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
            
            elif vendor_code and vendor_country:   
                if vendor_country == country_check  and  vendor_code == code_check   :
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
            else:
                if start_date == "" and end_date == "":
                    start_date="3000-05-01"
                    end_date="3000-05-01"
            
                if vendor_name == name_check or vendor_code == code_check or vendor_country == country_check or models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)) :
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                        "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                        "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
        
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})

        return JsonResponse({'message': 'No result Found'})


class activitySuspendedView(APIView):
    serializer_class = serializers.activitytypeSerializer
    
   
    @csrf_exempt
    def post(self,request):
        resultlist=[]
        print("hello")
        # user_obj=User.objects.get(id=user_id)
        # print("user_obj",user_obj.id)
        data=json.loads(request.body.decode('utf-8'))
        start_date=data["start_date"]
        print("start",start_date)
        end_date=data["end_date"]
        print(end_date)
        vendor_name = data["vendor_name"]
        print(type(vendor_name))
        vendor_code = data["vendor_code"]
        vendor_country=data["vendor_country"]
        print("country",vendor_country)
        if vendor_country == "":
            vendor_country=0
      
        w=Vendor.objects.filter(name=vendor_name).select_related('country')
        for i in w:
            print("ddmmm",i.country)  
        print("a",request.user.id)
        post=models.Activity.objects.filter(updated_by=1).select_related("vendor")
        post1=models.Activity.objects.filter(updated_by=1).values_list("activitytype",flat=True)
        post2=models.Activity.objects.filter(updated_by=1).values_list("title",flat=True)
        activitytitle=post2[0]
        post3=models.Activity.objects.filter(updated_by=1).values_list("code",flat=True)
        activitycode=post3[0]
        actitvitytype=post1[0]
        
        for i in post:
            name_check=str(i.vendor)
            print(type(name_check)) 
            if  (str(vendor_name) == name_check):
                print("done")
            status_check=str(i.vendor.vendor_status)
            id_vendor=str(i.vendor.vendor.id)
            print("qqqqqq",id_vendor)
        
            mt=UserProfile.objects.filter(user=id_vendor)
        for i in mt:
            code_check=str(i.code)
            print(code_check)
            country_check=str(i.country.id)
            country_name=str(i.country)
            print(country_check)

        if Vendor.objects.filter(vendor_status="SUSPENDED"):  
            if vendor_name and vendor_code and vendor_country and start_date and end_date:  
                if vendor_name == name_check and vendor_code == code_check and vendor_country == country_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                    "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
            
            elif vendor_name and vendor_code and start_date and end_date:  
                if vendor_name == name_check and vendor_code == code_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
            
            elif  vendor_country and vendor_code and start_date and end_date:  
                if vendor_country == country_check  and vendor_code == code_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
                
            elif  vendor_name and vendor_country and start_date and end_date:  
                if vendor_name == name_check  and  vendor_country == country_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
                
            elif vendor_name and  start_date and end_date:
                if vendor_name == name_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
                
            elif vendor_code and  start_date and end_date:
                if vendor_code == code_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})    
                
                
            elif vendor_country and  start_date and end_date:
                if vendor_country == country_check and models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)):  
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})        
                
            elif vendor_name and vendor_code and vendor_country:
                if vendor_name == name_check and vendor_code == code_check and vendor_country == country_check:
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
            
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})

            elif vendor_name and vendor_country :
                if vendor_name == name_check and  vendor_country == country_check :
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
            elif vendor_code and vendor_name:    
                if vendor_name == name_check and  vendor_code == code_check  :
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
            
            elif vendor_code and vendor_country:   
                if vendor_country == country_check  and  vendor_code == code_check   :
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                    "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                    "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})
            else:
                if start_date == "" and end_date == "":
                    start_date="3000-05-01"
                    end_date="3000-05-01"
            
                if vendor_name == name_check or vendor_code == code_check or vendor_country == country_check or models.Activity.objects.filter(updated_at__date__range=(start_date, end_date)) :
                    data = {
                    "vendor_name":name_check,
                    "status":status_check,
                        "vendor_code":code_check,
                    "country":country_name,
                    "activity_type":actitvitytype,
                    "activity_code":activitycode,
                    "activity_title":activitytitle,
                        "scheduled_classes":"1000",
                        "scheduled_session":"10000"
                    }
                    resultlist.append(data)
                    print("ss",resultlist)
        
                    return JsonResponse({'success': 'true','data' : data})
                else:
                    return JsonResponse({'message': 'False','data' : resultlist})

        return JsonResponse({'message': 'No result Found'})