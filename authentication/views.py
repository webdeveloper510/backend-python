from unicodedata import name
from django.http import JsonResponse
from django.db.models import Q
from typing_extensions import Self
from uuid import getnode
from simple_search import search_filter
import time
from rest_framework.decorators import api_view
import datetime
from datetime import date,timedelta
from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.schemas import openapi
from yaml import serialize
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from .serializers import RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, \
    EmailVerificationSerializer, LoginSerializer, LogoutSerializer,registerSerializer,activitySerializer,unactiveSerializer,statuscheck
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserProfile, userdetail,activity
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
from superadmin.subapps.countries_and_cities.models import Country, City


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    # renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        print("user is", user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        instance = User.objects.get(email=user_data['email'])
        if 'details' in user :
            country = Country.objects.get(name=user['details']['country'])
            city = City.objects.get(name=user['details']['city'])
            userdetails= UserProfile.objects.create(user=instance,firstname=user['details']['firstname'],
                                                    role=user['details']['type'],
                                                    lastname=user['details']['lastname'],country=country,city=city)
            userdetails.save()
        token = RefreshToken.for_user(instance).access_token
        #current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        # absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        # email_body = 'Hi ' + user.username + \
        #              ' Use the link below to verify your email \n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email,
        #         'email_subject': 'Verify your email'}
        #
        # Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        print("bjvbv",token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://' + current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                         absurl + "?redirect_url=" + redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url + '?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)




class check(generics.GenericAPIView):
    serializer_class = registerSerializer

    def get(self,request):
        a=request.user
        print("777777",a)
        user_obj = userdetail.objects.filter()
        print("111111",user_obj)
        return Response(status=status.HTTP_204_NO_CONTENT)




class activityView(generics.GenericAPIView):
    
    serializer_class = activitySerializer
    #renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        print("user is", user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)




class unactivityView(generics.GenericAPIView):
    serializer_class = unactiveSerializer

    def post(self,request):
        

        vendor = request.GET.get('start_date',False)
        vendor1 = request.GET.get('end_date', False)
        print("4444",vendor)
        print('hdfkdsjdvf',vendor1)
        vendor_obj= activity.objects.filter(created=[vendor,vendor1])
        print(vendor_obj)
        return Response({'message':'status is true'}, status=status.HTTP_200_OK)
        

class statuscheck(generics.GenericAPIView):
    serializer_class = statuscheck

    def post(self, request):
        vendor = request.data.get('vendor_name', '')
        current_user=activity.objects.filter(vendor_name=vendor).values_list("status",flat=True)
        if current_user.exists():
            current_user =current_user[0]
        else:
            current_user=""
        check_sta=current_user    
        if check_sta == True:
        
            return Response({'message':'status is true'}, status=status.HTTP_200_OK)
        elif check_sta == "":
            return Response({'error': 'vendor doesnot exists'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'status is False'},status=status.HTTP_400_BAD_REQUEST)    





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
                current_user=activity.objects.filter(created_at__date__range=(start_date, end_date))
                print("1",current_user)
            elif check :
                current_user1=activity.objects.filter( created_at__lte=datetime.date.today(),created_at__gt=datetime.date.today()-timedelta(days=30))
                print("2",current_user1)
            else:
                current_user2=activity.objects.filter( created_at__lte=datetime.date.today(),created_at__gt=datetime.date.today()-timedelta(days=60))
                print("3",current_user2)
        if type =="country":     
            print("hello4")
        elif type =="vendor_name" : 
            print(",,,,,,,,,,,,,,,,,,,,")  
        elif type =="vendor_code":
            print("777777777")     
           
    return JsonResponse({'success': 'true' })

#API for search 

@csrf_exempt
@api_view(['POST'])
def onlycheckuser(request):
    resultlist=[]
    search_fields = request.POST.get("vendor_name","")
    search_fields1 = request.POST.get("vendor_code","")
    search_fields2 = request.POST.get("country","")
    search_fields3 = request.POST.get("status")
    posts = activity.objects.filter(vendor_name=search_fields)| activity.objects.filter(vendor_code=search_fields1)|activity.objects.filter(country=search_fields2)|activity.objects.filter(status=search_fields3)
    print("===================================",posts)
    if posts:
           for project in posts:
                        data = {
                        "vendoe_name":project.vendor_name,
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
def searcheng(request):
    search_fields = request.POST.get("vendor_name","")
    search_fields1 = request.POST.get("vendor_code","")
    vendor = activity.objects.filter(Q(vendor_name__icontains=search_fields)|Q(vendor_code=search_fields1))
    print("++++++++++++++++++++++++++",vendor.query)
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