from django.views.decorators.csrf import csrf_exempt
import datetime
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response
from django.http import HttpResponse 
from .models import Vendor
from rest_framework import generics, status
from django.db.models import Q
from datetime import date,timedelta
import json
from .serializers import activityVendorSerializer


# @csrf_exempt
# def datecheck(request):
#     if request.method == "POST":
#         print("hello")
#         start_date=request.POST.get("start_date")
#         print("start",start_date)
#         end_date=request.POST.get("end_date")
#         print(end_date)
#         check=request.POST.get("check")
#         print("check",check)
        
#         type=request.POST.get("type")
#         print("type",type)
#         if type == "date":
#             if start_date and end_date:
#                 current_user=Vendor.objects.filter(created_at__date__range=(start_date, end_date))
#                 print("1",current_user)
#             elif check :
#                 current_user1=Vendor.objects.filter( created_at__lte=datetime.date.today(),created_at__gt=datetime.date.today()-timedelta(days=30))
#                 print("2",current_user1)
#             else:
#                 current_user2=Vendor.objects.filter( created_at__lte=datetime.date.today(),created_at__gt=datetime.date.today()-timedelta(days=60))
#                 print("3",current_user2)
           
           
#     return JsonResponse({'success': 'true' })

#API for search 

@csrf_exempt
@api_view(['POST'])
def onlycheckuser(request):
    resultlist=[]
    data=json.loads(request.body.decode('utf-8'))
    search_fields = data["vendor_name"]
    search_fields1 = data["organization_type"]
    search_fields2 = data["reg_zip_code"]
    posts = Vendor.objects.filter(vendor_name=search_fields)| Vendor.objects.filter(organization_type=search_fields1)|Vendor.objects.filter(reg_zip_code=search_fields2)
    print("===================================",posts)
    if posts:
           for project in posts:
                        data = {
                        "vendor_name":project.vendor_name,
                        "vendor_code":project.vendor_code,
                        "organization_type":project.organization_type,
                        "reg_address":project.reg_address,
                        "reg_city":project.reg_city,
                        "reg_zip_code":project.reg_zip_code,
                        "mailing_address":project.mailing_address,
                        "mailing_city":project.mailing_city,
                        "mailing_zip_code":project.mailing_zip_code,
                        "reg_number":project.reg_number,
                        "preferred_name":project.preferred_name,
                        "profile_intro":project.profile_intro,
                        "terms_and_conditions":project.terms_and_conditions,
                        "is_website":project.is_website,
                        "website_url":project.website_url,
                        "is_instagram":project.is_instagram,
                        "instagram_url":project.instagram_url,
                        "is_twitter":project.is_twitter,
                        "twitter_url":project.twitter_url,
                        "is_facebook":project.is_facebook,
                        "facebook_url":project.facebook_url,
                        "created":project.created,
                        "start_date":project.start_date,
                        "end_date":project.end_date,
                        "revenue":project.revenue,
                        "vendor_status":project.vendor_status,

                        }
                        resultlist.append(data)
           return JsonResponse({'success': 'true','data' : resultlist})
    else:
        return JsonResponse({'message': 'False','data' : resultlist})


@api_view(['POST'])
@csrf_exempt
def vendorDateApi(request):
    resultlist=[]
    data=json.loads(request.body.decode('utf-8'))
    start_date=data["start_date"]
    end_date=data["end_date"]
    date_check=data["date_check"]
    
    
    vendor_type=data["vendor_type"]
    vendor_name = data["vendor_name"]
    vendor_code = data["vendor_code"]
    country_field=data["mailing_zip_code"]
    if vendor_type =="vendor":
        posts = Vendor.objects.filter(vendor_name=vendor_name)| Vendor.objects.filter(vendor_code=vendor_code)| Vendor.objects.filter(mailing_zip_code=country_field)
        if posts:
            for project in posts:
                data = {
                        "vendor_name":project.vendor_name,
                        "vendor_code":project.vendor_code,
                        "organization_type":project.organization_type,
                        "reg_address":project.reg_address,
                        "reg_city":project.reg_city,
                        "reg_zip_code":project.reg_zip_code,
                        "mailing_address":project.mailing_address,
                        "mailing_city":project.mailing_city,
                        "mailing_zip_code":project.mailing_zip_code,
                        "reg_number":project.reg_number,
                        "preferred_name":project.preferred_name,
                        "profile_intro":project.profile_intro,
                        "terms_and_conditions":project.terms_and_conditions,
                        "is_website":project.is_website,
                        "website_url":project.website_url,
                        "is_instagram":project.is_instagram,
                        "instagram_url":project.instagram_url,
                        "is_twitter":project.is_twitter,
                        "twitter_url":project.twitter_url,
                        "is_facebook":project.is_facebook,
                        "facebook_url":project.facebook_url,
                        "created":project.created,
                        "start_date":project.start_date,
                        "end_date":project.end_date,
                        "revenue":project.revenue,
                        "vendor_status":project.vendor_status,
                }
                resultlist.append(data)
            return JsonResponse({'success': 'true','data' : resultlist})
        else:
            return JsonResponse({'message': 'False','data' : resultlist})
    

    if vendor_type == "date":
        if start_date and end_date:
            current_user=Vendor.objects.filter(created_at__date__range=(start_date, end_date))
            if current_user:
                for project in current_user:
                    data = {
                        "vendor_name":project.vendor_name,
                        "vendor_code":project.vendor_code,
                        "organization_type":project.organization_type,
                        "reg_address":project.reg_address,
                        "reg_city":project.reg_city,
                        "reg_zip_code":project.reg_zip_code,
                        "mailing_address":project.mailing_address,
                        "mailing_city":project.mailing_city,
                        "mailing_zip_code":project.mailing_zip_code,
                        "reg_number":project.reg_number,
                        "preferred_name":project.preferred_name,
                        "profile_intro":project.profile_intro,
                        "terms_and_conditions":project.terms_and_conditions,
                        "is_website":project.is_website,
                        "website_url":project.website_url,
                        "is_instagram":project.is_instagram,
                        "instagram_url":project.instagram_url,
                        "is_twitter":project.is_twitter,
                        "twitter_url":project.twitter_url,
                        "is_facebook":project.is_facebook,
                        "facebook_url":project.facebook_url,
                        "created":project.created,
                        "start_date":project.start_date,
                        "end_date":project.end_date,
                        "revenue":project.revenue,
                        "vendor_status":project.vendor_status,

                    }
                    resultlist.append(data)
                return JsonResponse({'success': 'true','data' : resultlist})
            else:
               return JsonResponse({'message': 'False','data' : resultlist})
        if date_check :
            current_user1=Vendor.objects.filter( created_at__lte=date.today(),created_at__gt=datetime.date.today()-timedelta(days=30))
            print("2",current_user1)
            if current_user1:
                for project in current_user1:
                    data = {
                        "vendor_name":project.vendor_name,
                        "vendor_code":project.vendor_code,
                        "organization_type":project.organization_type,
                        "reg_address":project.reg_address,
                        "reg_city":project.reg_city,
                        "reg_zip_code":project.reg_zip_code,
                        "mailing_address":project.mailing_address,
                        "mailing_city":project.mailing_city,
                        "mailing_zip_code":project.mailing_zip_code,
                        "reg_number":project.reg_number,
                        "preferred_name":project.preferred_name,
                        "profile_intro":project.profile_intro,
                        "terms_and_conditions":project.terms_and_conditions,
                        "is_website":project.is_website,
                        "website_url":project.website_url,
                        "is_instagram":project.is_instagram,
                        "instagram_url":project.instagram_url,
                        "is_twitter":project.is_twitter,
                        "twitter_url":project.twitter_url,
                        "is_facebook":project.is_facebook,
                        "facebook_url":project.facebook_url,
                        "created":project.created,
                        "start_date":project.start_date,
                        "end_date":project.end_date,
                        "revenue":project.revenue,
                        "vendor_status":project.vendor_status,


                    }
                    resultlist.append(data)
                return JsonResponse({'success': 'true','data' : resultlist})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
        
        else:
            current_user2=Vendor.objects.filter( created_at__lte=date.today(),created_at__gt=date.today()-timedelta(days=60))
            print("3",current_user2)
            if current_user2:
                for project in current_user2:
                    data = {
                        "vendor_name":project.vendor_name,
                        "vendor_code":project.vendor_code,
                        "organization_type":project.organization_type,
                        "reg_address":project.reg_address,
                        "reg_city":project.reg_city,
                        "reg_zip_code":project.reg_zip_code,
                        "mailing_address":project.mailing_address,
                        "mailing_city":project.mailing_city,
                        "mailing_zip_code":project.mailing_zip_code,
                        "reg_number":project.reg_number,
                        "preferred_name":project.preferred_name,
                        "profile_intro":project.profile_intro,
                        "terms_and_conditions":project.terms_and_conditions,
                        "is_website":project.is_website,
                        "website_url":project.website_url,
                        "is_instagram":project.is_instagram,
                        "instagram_url":project.instagram_url,
                        "is_twitter":project.is_twitter,
                        "twitter_url":project.twitter_url,
                        "is_facebook":project.is_facebook,
                        "facebook_url":project.facebook_url,
                        "created":project.created,
                        "start_date":project.start_date,
                        "end_date":project.end_date,
                        "revenue":project.revenue,
                        "vendor_status":project.vendor_status,


                    }
                    resultlist.append(data)
                return JsonResponse({'success': 'true','data' : resultlist})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
    
    if vendor_type == "reg_zip_code":  

            current_user5=Vendor.objects.filter(country=country_field)
            print("41",current_user5)
            if current_user5:
                for project in current_user5:
                    data = {
                        "vendor_name":project.vendor_name,
                        "vendor_code":project.vendor_code,
                        "organization_type":project.organization_type,
                        "reg_address":project.reg_address,
                        "reg_city":project.reg_city,
                        "reg_zip_code":project.reg_zip_code,
                        "mailing_address":project.mailing_address,
                        "mailing_city":project.mailing_city,
                        "mailing_zip_code":project.mailing_zip_code,
                        "reg_number":project.reg_number,
                        "preferred_name":project.preferred_name,
                        "profile_intro":project.profile_intro,
                        "terms_and_conditions":project.terms_and_conditions,
                        "is_website":project.is_website,
                        "website_url":project.website_url,
                        "is_instagram":project.is_instagram,
                        "instagram_url":project.instagram_url,
                        "is_twitter":project.is_twitter,
                        "twitter_url":project.twitter_url,
                        "is_facebook":project.is_facebook,
                        "facebook_url":project.facebook_url,
                        "created":project.created,
                        "start_date":project.start_date,
                        "end_date":project.end_date,
                        "revenue":project.revenue,
                        "vendor_status":project.vendor_status,

                    }
                    resultlist.append(data)
                return JsonResponse({'success': 'true','data' : resultlist})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
    if vendor_type == "revenue":
            current_user6=Vendor.objects.all().order_by('-revenue')
            print("4",current_user6)
            if current_user6:
                for project in current_user6:
                    data = {
                        "vendor_name":project.vendor_name,
                        "vendor_code":project.vendor_code,
                        "organization_type":project.organization_type,
                        "reg_address":project.reg_address,
                        "reg_city":project.reg_city,
                        "reg_zip_code":project.reg_zip_code,
                        "mailing_address":project.mailing_address,
                        "mailing_city":project.mailing_city,
                        "mailing_zip_code":project.mailing_zip_code,
                        "reg_number":project.reg_number,
                        "preferred_name":project.preferred_name,
                        "profile_intro":project.profile_intro,
                        "terms_and_conditions":project.terms_and_conditions,
                        "is_website":project.is_website,
                        "website_url":project.website_url,
                        "is_instagram":project.is_instagram,
                        "instagram_url":project.instagram_url,
                        "is_twitter":project.is_twitter,
                        "twitter_url":project.twitter_url,
                        "is_facebook":project.is_facebook,
                        "facebook_url":project.facebook_url,
                        "created":project.created,
                        "start_date":project.start_date,
                        "end_date":project.end_date,
                        "revenue":project.revenue,
                        "vendor_status":project.vendor_status,


                    }
                    resultlist.append(data)
                return JsonResponse({'success': 'true','data' : resultlist})
            else:
                return JsonResponse({'message': 'False','data' : resultlist})
    return JsonResponse({"message":"Please enter the type"}) 



# @csrf_exempt
# @api_view(['POST'])
# def search(request):
#     resultlist = []
#     search_fields = request.POST.get("search")
    
#     shipper = Vendor.objects.filter(Q(vendor_name__icontains=search_fields)|Q(country__icontains=search_fields)|Q(revenue__icontains=search_fields)|Q(vendor_code__icontains=search_fields))
#     print(shipper)

#     if shipper:
#         for project in shipper:
#                         data = {
#                         "vendor_name":project.vendor_name,
#                         "vendor_code":project.vendor_code,
#                         "country":project.country,
#                         "status":project.status,
#                         "activity_title":project.activity_title,
#                         "activity_code":project.activity_code,
#                         "revenue":project.revenue,
#                         "number_of_registration":project.session_of_classes,
#                         "revenue_per_registration":project.available_future_sessions
#                         }
#                         resultlist.append(data)
#         return JsonResponse({'success': 'true','data' : resultlist})
#     else:
#         return JsonResponse({'message': 'False','data' : resultlist})




# @csrf_exempt
# @api_view(['POST'])
# def vendorsearch(request):
#     search_fields = request.POST.get("vendor_name","")
#     search_fields1 = request.POST.get("vendor_code","")
#     search_fields2 = request.POST.get("reg_zip_code","")
#     vendor = Vendor.objects.filter(Q(vendor_name__icontains=search_fields)|Q(vendor_code=search_fields1))|Q(reg_zip_code=search_fields2)
#     print("++++++++++++++++++++++++++",vendor)
#     return JsonResponse({'success': 'true' })



# @csrf_exempt
# def download_file(request):
#     filename  = "C:\\Users\Ashpreet\\Desktop\\new_back\\moppetto-backend\\totals.csv" 
#     download_name ="example.xlsx"
#     with open(filename, 'r') as f:
#         file_data = f.read()
#     response = HttpResponse(file_data, content_type='text/csv')
#     response['Content-Disposition'] = "attachment; filename=%s"%download_name
    
#     return response    


class activityVendorView(generics.GenericAPIView):
    
    serializer_class = activityVendorSerializer
    #renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        print("user is", user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)