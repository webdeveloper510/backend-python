from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from rest_framework import serializers as serializers_drf

# from superadmin.subapps.countries_and_cities import serializers as serializers_country
# from superadmin.subapps.countries_and_cities import models as models_country

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# For HTTP Error
from rest_framework import status,generics
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator
from rest_framework.settings import api_settings
from rest_framework_csv import renderers as r
import csv

from superadmin.permissions_api import IsPostOrIsAuthenticated
from django.contrib.auth import password_validation
from django.core import exceptions

from superadmin.subapps.countries_and_cities import models as models_country
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator
from django.db.models import ProtectedError
from vendor.subapps.profile import models as VendorProfileModels
from vendor.subapps.profile import profile_serializers as VendorProfileSerializers
from authentication import responses


class Vendors(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        obj = VendorProfileModels.VendorProfile.objects.all()
        if ('country' in request.GET):
            country = request.GET['country']
            try:
                c = models_country.Country.objects.get(name=country)
            except:
                return Response({"error":'country object does not exists'},status=status.HTTP_404_NOT_FOUND)
            obj = obj.filter(vendor__userdetails__country=c)
        if ('status' in request.GET):
            vstatus = request.GET['status']
            if (vstatus in dict(VendorProfileModels.VENDOR_STATUS).keys()):
                obj = obj.filter(vendor_status=vstatus)
            else:
                return Response({"error":'the param "status" has invalid value'},status=status.HTTP_400_BAD_REQUEST)

        paginator = CustomLimitOffsetPaginator()
        if (request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(obj, request, view=self)
            serializer = VendorProfileSerializers.VendorProfileSerializer(
                page, many=True)
            if page is not None:
                entityCount=obj.filter(organization_type="ENTITY").count()
                indCount=obj.filter(organization_type="INDIVIDUAL").count()
                return paginator.get_paginated_response(serializer.data,entityCount=entityCount,indCount=indCount)
        else:
            serializer = VendorProfileSerializers.VendorProfileSerializer(obj, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = serializers.VendorSerializer(data=request.data)
        if (serializer.is_valid()):
            obj = serializer.save()
            try:
                pass
            except:
                return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Vendor(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            obj = VendorProfileModels.VendorProfile.objects.get(id=id)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorProfileSerializers.VendorProfileSerializer(obj)
        return Response(serializer.data)

    def patch(self, request, id):
        try:
            obj = VendorProfileModels.VendorProfile.objects.get(id=id)
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorProfileSerializers.VendorProfileSerializer(
            obj, data=request.data, partial=True)
        if (serializer.is_valid()):
            try:
                serializer.save()
            except:
                return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterVendorSubscriptionRenderer(r.CSVRenderer):
    header = [
        # 'id',
        'legal_name',
        'email',
        'name',
        'vendor_status',
        'organization_type',
        'entity_reg_number',
        'country',
        'city',
        'code',
        'created_at',
        # 'logo',
        # 'logo.file',
        # 'mailing_address',
        'mailing_address.address_line_1',
        'mailing_address.address_line_2',
        # 'mailing_address.phone_mobile',
        # 'mailing_address.phone_office',
        'mailing_address.zipcode',
        # 'registered_address',
        'registered_address.address_line_1',
        'registered_address.address_line_2',
        'registered_address.phone_mobile',
        # 'registered_address.phone_office',
        # 'registered_address.zipcode',
        # 'profile_intro',
        # 'terms',
        # 'video_introduction_url',
        'website',
    ]
    labels = {
        'mailing_address.address_line_1': "Mailing Address Line 1",
        'mailing_address.address_line_2': "Mailing Address Line 2",
        'mailing_address.phone_mobile': "Mailing Address Mobile Phone",
        'mailing_address.phone_office': "Mailing Address Office Phone",
        'mailing_address.zipcode': "Mailing Address Zipcode",

        'registered_address.address_line_1': "Registered Address Line 1",
        'registered_address.address_line_2': "Registered Address Line 2",
        'registered_address.phone_mobile': "Registered Address Mobile Phone",
        'registered_address.phone_office': "Registered Address Office Phone",
        'registered_address.zipcode': "Registered Address Zipcode",
    }


class VendorsCSV(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)
    renderer_classes = (FilterVendorSubscriptionRenderer,) + \
        tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    # renderer_classes = (FilterVendorSubscriptionRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def get(self, request):
        obj = VendorProfileModels.VendorProfile.objects.all()
        if ('status' in request.GET):
            status = request.GET['status']
            if (status in dict(VendorProfileModels.VENDOR_STATUS).keys()):
                obj = obj.filter(vendor_status=status)
            else:
                return Response(responses.create_failure_response("the param 'status' has invalid value"))

        serializer = VendorProfileSerializers.VendorProfileSerializer(obj, many=True)
        return Response(serializer.data)


class Users(APIView):
    # To allow authenticated users only
    permission_classes = (IsPostOrIsAuthenticated,)

    def get(self, request):
        obj = models.User.objects
        if ('city' in request.GET):
            city = request.GET['city']
            try:
                c = models_country.City.objects.get(name=city)
            except:
                return Response(responses.create_failure_response('city object does not exists'))
            obj = obj.filter(userdetails__city=c)

        paginator = CustomLimitOffsetPaginator()
        if (request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(obj, request, view=self)
            serializer = serializers.UserRegistrationSerializer(
                page, many=True)
            if page is not None:
                return paginator.get_paginated_response(serializer.data)
        else:
            serializer = serializers.UserRegistrationSerializer(obj, many=True)
            return Response(serializer.data)

    def post(self, request):
        print("coming here", request.data)
        serializer = serializers.UserDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # try:
        obj = serializer.save()

        # except Exception as e:
        #     print(e)
        #     return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class User(APIView):
    # To allow authenticated users only
    # permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            obj = models.User.objects.get(id=id, userdetails__role="CONSUMER")
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserRegistrationSerializer(obj)
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            obj = models.User.objects.get(id=id, userdetails__role="CONSUMER")
            obj.delete()
            return Response(responses.create_success_response('object deleted successfully'))

        except ProtectedError as e:
            return Response(responses.create_failure_response('this object is currently being used. ' + str(e)))

        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            obj = models.User.objects.get(id=id, userdetails__role="CONSUMER")
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserRegistrationSerializer(
            obj, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            try:
                pass
            except:
                return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FamilyRenderer(r.CSVRenderer):
    # header = ['superadmin.first_name, admin']
    # header = ['superadmin.email','superadmin.first_name','superadmin.last_name','admin','kids.0.age','kids.0.image','kids.0.name','kids.1.age','kids.1.image','kids.1.name','ongoing_activities','past_activities','status']
    labels = {
        # 'SubscriptionPricing.no_of_activities': 'no_of_activities',
    }

class ChangeFamilyStatus(APIView):
    permisson_classes = [IsAuthenticated]
    def patch(self,request,id):
        fstatus = request.data.get('status')
        if fstatus == None:
            return Response({"status":"This field is required."},status=status.HTTP_400_BAD_REQUEST)
        if fstatus not in dict(models.FAMILY_STATUS).keys():
            return Response({"status":"Invalid Status"},status=status.HTTP_400_BAD_REQUEST)
        

        try:
            family = models.Family.objects.get(id=id)
            family.status = fstatus
            family.save()
        except models.Family.DoesNotExist:
            return Response({"error":"Family objects not found"},status=status.HTTP_404_NOT_FOUND)

        return Response({"message":"Status Updated Successfully"})

class Families(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    # renderer_classes = (FamilyRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def get(self, request):
        obj = models.Family.objects.all()
        # obj = models.Family.objects.all()[:100]
        country = request.GET.get('country')
        if country is None:
            return Response({'successs': False, 'message': 'country is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if request.GET.get('code'):
            try:
                user = models.UserDetail.objects.get(
                    code=request.GET.get('code'))
                obj = obj.filter(Q(superadmin=user.user) | Q(admin=user.user))
            except Exception as e:
                print(e)
                return Response({'successs': False, 'message': 'User can not find'}, status=status.HTTP_404_NOT_FOUND)
        paginator = CustomLimitOffsetPaginator()
        if (request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            # paginator = LimitOffsetPagination()
            page = paginator.paginate_queryset(obj, request, view=self)
            serializer = serializers.FamilySerializer(
                page, many=True)
            if page is not None:
                resultsCount = obj.filter(Q(superadmin__userdetails__country__name=country)|Q(admin__userdetails__country__name=country)).count()
                usersCount = obj.count()
                response = paginator.get_paginated_response(serializer.data,resultsCount=resultsCount,usersCount=usersCount)
                print(response)
                return response
        else:
            serializer = serializers.FamilySerializer(
                obj, many=True)
            return Response(serializer.data)


class FamiliesCSV(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        model = models.Family
        objs = models.Family.objects.all()
        response = HttpResponse(content_type='text/csv')
        # force download
        # response['Content-Disposition'] = 'attachment; filename={}.csv'.format(file_name)
        # the csv writer
        writer = csv.writer(response)

        titles = ['superadmin', 'superadmin email', 'admin', 'admin email', 'kid name', 'kid id', 'kid age',
                  'ongoing/upcoming activities', 'past activities', 'status']

        writer.writerow(titles)

        for obj in objs:
            if (obj.superadmin):
                superadmin = obj.superadmin.get_full_name()
                superadmin_email = obj.superadmin.username
            else:
                superadmin = ''
                superadmin_email = ''

            if (obj.admin):
                admin = obj.admin.get_full_name()
                admin_email = obj.admin.username
            else:
                admin = ''
                admin_email = ''

            writer.writerow([superadmin, superadmin_email, admin, admin_email, '', '', '', obj.upcoming_activities,
                             obj.past_activities, obj.status])
            for kid in obj.kids.all():
                writer.writerow(['', '', '', '', kid.name,
                                kid.id, kid.age, "", "", ""])

        return response


class UserProfile(APIView):
    # To allow authenticated users only
    # permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            obj = models.User.objects.get(id=id, userdetails__role="CONSUMER")
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(obj)
        return Response(serializer.data)

    def patch(self, request, id):
        try:
            obj = models.User.objects.get(id=id, userdetails__role="CONSUMER")
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(
            obj, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            try:
                pass
            except:
                return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserProfile(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = serializers.UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = serializers.UpdateUserProfileSerializer(
            request.user, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            try:
                pass
            except:
                return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserFamily(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    # renderer_classes = (FamilyRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def get(self, request):
        family = request.user.userdetails.family
        # obj = models.Family.objects.all()
        user = request.user
        if (family == None):
            family = models.Family.objects.create(
                superadmin=user, status="ACTIVE")
            user.userdetails.family = family
            user.userdetails.save(update_fields=["family"])

        serializer = serializers.FamilySerializer(family, many=False)
        return Response(serializer.data)

    def patch(self, request):
        try:
            family = request.user.userdetails.family
            if (family == None):
                family = models.Family.objects.create(
                    superadmin=request.user, status="ACTIVE")
                request.user.userdetails.family = family
                request.user.userdetails.save(update_fields=["family"])
        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.FamilySerializer(
            family, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            try:
                pass
            except:
                return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentFamilyKids(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    # renderer_classes = (FamilyRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def post(self, request):
        if (request.user.userdetails.family == None):
            return Response(responses.create_failure_response('curren user dont have a family'),
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.KidSerializer(data=request.data)

        if (serializer.is_valid()):
            obj = serializer.save()
            obj.family = request.user.userdetails.family
            obj.save(update_fields=["family"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentFamilyKid(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    def delete(self, request, id):
        try:
            obj = models.Kid.objects.get(
                id=id, family=request.user.userdetails.family)
            if obj.image and (obj.avatar == None):
                obj.image.status = "INACTIVE"
                obj.image.save(update_fields=["status"])

            obj.delete()
            return Response(responses.create_success_response('object deleted successfully'))

        except ProtectedError as e:
            return Response(responses.create_failure_response('this object is currently being used. ' + str(e)))

        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            obj = models.Kid.objects.get(
                id=id, family=request.user.userdetails.family)

        except:
            return Response(responses.RESP_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.KidSerializer(
            obj, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            try:
                pass
            except:
                return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    # renderer_classes = (FamilyRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)

    def post(self, request):
        if ('old_password' not in request.data):
            return Response(responses.create_failure_response('old_password field is required'),
                            status=status.HTTP_400_BAD_REQUEST)
        if ('new_password' not in request.data):
            return Response(responses.create_failure_response('new_password field is required'),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # validate the password and catch the exception
            password_validation.validate_password(
                password=request.data['new_password'], user=models.User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            # errors['new_password'] = list(e.messages)
            raise serializers_drf.ValidationError(
                {'new_password': [e.messages]})

        if (request.user.check_password(request.data['old_password'])):

            request.user.set_password(request.data['new_password'])
            request.user.save()
            print(request.user.check_password(request.data['new_password']))
            return Response(responses.create_success_response('password changed successfully'))

        return Response(responses.create_failure_response('old_password is invalid'),
                        status=status.HTTP_400_BAD_REQUEST)
