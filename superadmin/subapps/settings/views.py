from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import models
from superadmin.subapps.vendor_and_user_management import models as models_users
from . import serializers
from superadmin.subapps.vendor_and_user_management import serializers as serializers_users
from rest_framework import serializers as serializers_drf

from rest_framework.views import APIView
from . import models
# For HTTP Error
from rest_framework import status
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator

from django.http import HttpResponse

from django.utils.decorators import method_decorator
from superadmin import decorators

from django.core.validators import EmailValidator
import secrets
from django.utils import timezone
from authentication import responses

from superadmin.subapps.countries_and_cities import models as models_country
from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator

# ============================================
#               Superadmin
# ============================================

class SuperadminUserFeedback(APIView):
    # To allow authenticated users only

    # @method_decorator(decorators.log_db_read_operation)
    def get(self, request):
        feedback = models.UserFeedback.objects.all()
        if("country" in request.GET):
            # return Response(responses.create_failure_response("parameter country is required."), status=status.HTTP_400_BAD_REQUEST )
            country_name = request.GET['country']
            try:
                country = models_country.Country.objects.get(name=country_name)
                # country = models_country.Country.objects.filter(name=country_name, status="ACTIVE")
            except:
                return Response(responses.create_failure_response("country does not exists or it is inactive."), status=status.HTTP_404_NOT_FOUND)
            feedback = feedback.filter(user__userdetails__country=country )
        
            if("city" in request.GET):
                city = request.GET['city']
                city_name = request.GET['city']
                try:
                    city = models_country.City.objects.get(name=city_name, country=country)
                except:
                    return Response(responses.create_failure_response("city does not exists or it is inactive."), status=status.HTTP_404_NOT_FOUND)
                feedback = feedback.filter(user__userdetails__city = city )

        paginator = CustomLimitOffsetPaginator()
        if(request.GET.get(CustomLimitOffsetPaginator.limit_query_param, False)):
            page = paginator.paginate_queryset(feedback, request, view=self)
            serializer = serializers.SuperadminUserFeedbackSerializer(
                page, many=True
                )
            if page is not None:
                return paginator.get_paginated_response(serializer.data)
        else:
            serializer = serializers.SuperadminUserFeedbackSerializer(feedback, many=True)
            return Response(serializer.data)




# ============================================


class CurrentUserFeedback(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)

    @method_decorator(decorators.log_db_read_operation)
    def get(self, request):
        feedback = models.UserFeedback.objects.filter(user = request.user)
        serializer = serializers.UserFeedbackSerializer(feedback, many=True)
        return Response(serializer.data)
        # return Response({})
    
    @method_decorator(decorators.log_db_create_operation)
    def post(self, request):
        serializer = serializers.UserFeedbackSerializer(data=request.data)
        if(serializer.is_valid()):
            obj = serializer.save()
            obj.user = request.user
            obj.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddAdmin(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)
    # @method_decorator(decorators.log_db_read_operation)

    def post(self, request):
        if(request.user.userdetails.role != "CONSUMER"):
            raise serializers_drf.ValidationError(
                {"permission error": "only Moppetto users can send invitation"})

        if('email' not in request.data):
            raise serializers_drf.ValidationError(
                {"email": "field email is required"})
        if('rights' not in request.data):
            raise serializers_drf.ValidationError(
                {"rights": "field rights is required"})

        email = request.data.get('email')
        rights = request.data.get('rights')

        validator = EmailValidator()
        try:
            validator(email)
        except:
            return Response(responses.create_failure_response('invalid email address'))

        if(rights not in dict(models.TARGET_RIGHTS).keys()):
            return Response(responses.create_failure_response('invalid rights'))

        while(True):
            token = secrets.token_urlsafe()
            print(token)
            print(len(token))
            matches = models.UserAdminInvitation.objects.filter(
                status="ACTIVE", token=token)
            if(not matches.exists()):
                break

        invitation = models.UserAdminInvitation.objects.create(sender=request.user,
                                                               recepient_email=email,
                                                               token=token,
                                                               status="ACTIVE",
                                                               target_rights=rights)

        invitation.send_email(request)
        serializer = serializers.InvitationSerializer(invitation)
        return Response({'status': True, "message": 'invitation sent successfully', "data": serializer.data})

class CancelInvitationOfUser(APIView):
    # To allow authenticated users only
    permission_classes = (IsAuthenticated,)
    # @method_decorator(decorators.log_db_read_operation)

    def post(self, request, id):
        if(request.user.userdetails.role != "CONSUMER"):
            raise serializers_drf.ValidationError(
                {"permission error": "only Moppetto users can send invitation"})

        try:
            invitation = models.UserAdminInvitation.objects.get(id=id, sender=request.user)
            invitation.status= 'CANCEL'
            invitation.save()

        except models.UserAdminInvitation.DoesNotExist:
            return Response({'error': 'Admin can not find.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.InvitationSerializer(invitation)
        return Response({'status': True, "message": 'invitation sent successfully', "data": serializer.data})



class InvitationLandingPage(APIView):
    def get(self, request, token):
        matches = models.UserAdminInvitation.objects.filter(
                status="ACTIVE", token=token)
        if(not matches.exists()):
            return HttpResponse(responses.RESP_NOT_FOUND['message'], status=status.HTTP_404_NOT_FOUND)
        
        invitation = matches.first()
        return HttpResponse("it worked " + str(token))


class RegisterInvitedUser(APIView):
    # To allow authenticated users only
    # permission_classes = (IsPostOrIsAuthenticated,)
    
    def post(self, request):
        if('token' not in request.data):
            return Response(responses.create_success_response('token is not supplied'), status=status.HTTP_400_BAD_REQUEST)
        
        token = request.data.pop('token')

        # Get Invitation object associated with token
        matches = models.UserAdminInvitation.objects.filter(status="ACTIVE", token=token)
        if(not matches.exists()):
            return Response(responses.create_failure_response("Invitation not found"), status=status.HTTP_404_NOT_FOUND)
        invitation = matches.first()

        request.data['email'] = invitation.recepient_email
        
        # register user
        serializer = serializers_users.UserRegistrationSerializer(data=request.data)
        if(serializer.is_valid()):
            # print("valid")
            obj = serializer.save()
            obj.userdetails.family = invitation.sender.userdetails.family
            if(invitation.target_rights == "SUPERUSER"):
                invitation.sender.userdetails.family.admin = invitation.sender
                invitation.sender.userdetails.family.superadmin = obj

                
            else:
                invitation.sender.userdetails.family.admin = obj

            # print(obj.userdetails.family)
            invitation.sender.userdetails.family.save(update_fields=['admin', 'superadmin'])
            

            obj.userdetails.rights = invitation.target_rights
            obj.userdetails.save(update_fields=["family",'rights'])

            invitation.accepted_at = timezone.now()
            invitation.status = "ACCEPTED"
            invitation.recepient_user = obj
            invitation.save(update_fields=["accepted_at",'status', 'recepient_user'])

            try:
                pass
            except:
                return Response(responses.RESP_INTERNAL_SERVER_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
