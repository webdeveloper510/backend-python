from rest_framework import status
from rest_framework.response import Response
from superadmin.subapps.vendor_and_user_management import models as models_vendors


def only_vendor_allowed(function):
    def wrap(request, *args, **kwargs):
        if(request.user.userdetails.role != "VENDOR" or not models_vendors.Vendor.objects.filter(user=request.user).exists()):
            return Response(responses.create_failure_response('only vendors can access this apis'), status=status.HTTP_403_FORBIDDEN)
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    return wrap


def only_superAdmin_adminStaff_allowed(function):
    def wrap(request, *args, **kwargs):
        
        admin=False
        if(request.user.is_superuser or request.user.is_staff):
            return function(request, *args, **kwargs)
        return Response(responses.create_failure_response('only super-admin and sub-admin can access this apis'), status=status.HTTP_403_FORBIDDEN)

    wrap.__doc__ = function.__doc__
    return wrap


def only_superAdmin_allowed(function):
    def wrap(request, *args, **kwargs):
        if(request.user.is_superuser):
            return function(request, *args, **kwargs)
        return Response(responses.create_failure_response('only super-admin can access this apis'), status=status.HTTP_403_FORBIDDEN)

    wrap.__doc__ = function.__doc__
    return wrap
