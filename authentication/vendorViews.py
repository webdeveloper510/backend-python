from django.views.decorators.csrf import csrf_exempt
import datetime
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.http import HttpResponse 
from .models import Vendor
from django.db.models import Q
from datetime import date,timedelta
import json

@csrf_exempt
def datecheck(request):
    if request.method == "POST":
        print("hello")
        start_date=request.POST.get("start_date")
        print("start",start_date)
        end_date=request.POST.get("end_date")
        print(end_date)
        check=request.POST.get("check")
        print("check",check)
        
        type=request.POST.get("type")
        print("type",type)
        if type == "date":
            if start_date and end_date:
                current_user=Vendor.objects.filter(created_at__date__range=(start_date, end_date))
                print("1",current_user)
            elif check :
                current_user1=Vendor.objects.filter( created_at__lte=datetime.date.today(),created_at__gt=datetime.date.today()-timedelta(days=30))
                print("2",current_user1)
            else:
                current_user2=Vendor.objects.filter( created_at__lte=datetime.date.today(),created_at__gt=datetime.date.today()-timedelta(days=60))
                print("3",current_user2)
           
           
    return JsonResponse({'success': 'true' })

#API for search 

@csrf_exempt
@api_view(['POST'])
def onlycheckuser(request):
    resultlist=[]
    data=json.loads(request.body.decode('utf-8'))
    search_fields = data["vendor_name"]
    search_fields1 = data["vendor_code"]
    search_fields2 = data["reg_zip_code"]
    posts = Vendor.objects.filter(vendor_name=search_fields)| Vendor.objects.filter(vendor_code=search_fields1)|Vendor.objects.filter(reg_zip_code=search_fields2)
    print("===================================",posts)
    if posts:
           for project in posts:
                        data = {
                        "vendor_name":project.vendor_name,
                        "vendor_code":project.vendor_code,
                        "country":project.country,
                        "status":project.status,
                        "activity_title":project.activity_title,
                        "activity_code":project.activity_code,
                        "revenue":project.revenue,
                        "number_of_registration":project.session_of_classes,
                        "revenue_per_registration":project.available_future_sessions
                        }
                        resultlist.append(data)
           return JsonResponse({'success': 'true','data' : resultlist})
    else:
        return JsonResponse({'message': 'False','data' : resultlist})





@csrf_exempt
@api_view(['POST'])
def search(request):
    resultlist = []
    search_fields = request.POST.get("search")
    
    shipper = Vendor.objects.filter(Q(vendor_name__icontains=search_fields)|Q(country__icontains=search_fields)|Q(revenue__icontains=search_fields)|Q(vendor_code__icontains=search_fields))
    print(shipper)

    if shipper:
        for project in shipper:
                        data = {
                        "vendor_name":project.vendor_name,
                        "vendor_code":project.vendor_code,
                        "country":project.country,
                        "status":project.status,
                        "activity_title":project.activity_title,
                        "activity_code":project.activity_code,
                        "revenue":project.revenue,
                        "number_of_registration":project.session_of_classes,
                        "revenue_per_registration":project.available_future_sessions
                        }
                        resultlist.append(data)
        return JsonResponse({'success': 'true','data' : resultlist})
    else:
        return JsonResponse({'message': 'False','data' : resultlist})




@csrf_exempt
@api_view(['POST'])
def vendorsearch(request):
    search_fields = request.POST.get("vendor_name","")
    search_fields1 = request.POST.get("vendor_code","")
    search_fields2 = request.POST.get("reg_zip_code","")
    vendor = Vendor.objects.filter(Q(vendor_name__icontains=search_fields)|Q(vendor_code=search_fields1))|Q(reg_zip_code=search_fields2)
    print("++++++++++++++++++++++++++",vendor)
    return JsonResponse({'success': 'true' })



@csrf_exempt
def download_file(request):
    filename  = "C:\\Users\Ashpreet\\Desktop\\new_back\\moppetto-backend\\totals.csv" 
    download_name ="example.xlsx"
    with open(filename, 'r') as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    
    return response    