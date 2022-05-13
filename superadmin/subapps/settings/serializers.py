from rest_framework import serializers
from . import models
from superadmin import custom_serializers_fields as csf

class UserFeedbackSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    class Meta:
        model = models.UserFeedback
        fields = ('id','feedback', 'created_at', 'updated_at')
    
    def get_created_at(self, obj):
        return obj.created_at.isoformat()

        
    def get_updated_at(self, obj):
        return obj.updated_at.isoformat()



class SuperadminUserFeedbackSerializer(serializers.ModelSerializer):
    userid = csf.ReadWriteSerializerMethodField(allow_null=True, required=False)
    first_name = csf.ReadWriteSerializerMethodField(allow_null=True, required=False)   
    last_name = csf.ReadWriteSerializerMethodField(allow_null=True, required=False)   
    email = csf.ReadWriteSerializerMethodField(allow_null=True, required=False)    
    country = csf.ReadWriteSerializerMethodField(allow_null=True, required=False)    
    city = csf.ReadWriteSerializerMethodField(allow_null=True, required=False)   
    # date =  csf.ReadWriteSerializerMethodField(allow_null=True, required=False)   
    # time = csf.ReadWriteSerializerMethodField(allow_null=True, required=False)   
    created = serializers.SerializerMethodField()
    class Meta:
        model = models.UserFeedback
        fields = ('userid', 'first_name', 'last_name', 'email', 'country', 'city' ,'feedback', 'created')
    
    def get_created(self, obj):
        return obj.created_at.isoformat()


    def get_userid(self, obj):
        if (obj.user):
            return obj.user.id
        else:
            return None
    
    def get_username(self, obj):
        if (obj.user):
            return obj.user.username
        else:
            return None

    def get_first_name(self, obj):
        if (obj.user):
            return obj.user.first_name
        else:
            return None
    
    def get_last_name(self, obj):
        if (obj.user):
            return obj.user.last_name
        else:
            return None

    def get_email(self, obj):
        if (obj.user):
            return obj.user.email
        else:
            return None

    def get_country(self, obj):
        if (obj.user):
            if(obj.user.userdetails.role == "VENDOR"):
                print("I am here")
                if(obj.user.userdetails.vendor and self.user.userdetails.vendor.country):
                    return obj.user.userdetails.vendor.country
                else:
                    return None
            else:
                if(obj.user.userdetails.country):
                    return obj.user.userdetails.country.name
                else:
                    return None
        else:
            return None
    
    def get_city(self, obj):
        if (obj.user):
            if(obj.user.userdetails.role == "VENDOR"):
                if(obj.user.userdetails.vendor and obj.user.userdetails.vendor.city):
                    return obj.user.userdetails.vendor.city
                else:
                    return None
            else:
                if(obj.user.userdetails.city):
                    return obj.user.userdetails.city.name
                else:
                    return None
        else:
            return None

    # def get_date(self, obj):
    #     if (obj.created_at):
    #         return obj.created_at.date()
    #     else:
    #         return None
    
    # def get_time(self, obj):
    #     if (obj.created_at):
    #         return obj.created_at.time().replace(microsecond=0)
    #     else:
    #         return None


class InvitationSerializer(serializers.ModelSerializer):
    invitation_status = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = models.UserAdminInvitation
        fields=['id', 'recepient_email', 'recepient_user',
        'target_rights', 'token', 'invitation_status', "status", 'created_at', 'accepted_at']
        extra_kwargs ={
            'status': {'write_only': True}
        }
    
    def get_invitation_status(self, obj):
        if obj.status == 'ACTIVE':
            return 'SENT'
        return obj.status

    def get_created_at(self, obj):
        return obj.created_at.isoformat()