from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers_activity as serializers
from . import serializers_slots
from . import models
from django.utils.decorators import method_decorator
from superadmin import decorators
from superadmin.subapps.vendor_and_user_management import models as models_vendors
from vendor.subapps.profile import models as models_profile
from authentication import decorators as auth_decorators,responses
from django.shortcuts import get_object_or_404



def serialize_location_slots(objs, locations, activity,subscription_end_date):
    resp = []
    for location in locations:
        loc = {
            "location": location.shortname,
            "expirydate": subscription_end_date,   # depends on Vendor Subscription
            "slots": []
        }
        slots = objs.filter(location=location, activity=activity)
        serializer = serializers_slots.SlotSerializer(slots, many=True)
        loc["slots"] = serializer.data
        resp.append(loc)

    return resp


class Slots(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, id):
        objs = models.Slot.objects.all()
        try:
            activity = get_object_or_404(models.Activity, id=id)
            # pass
        except:
            return Response(responses.create_failure_response('activity object not found'), status=status.HTTP_404_NOT_FOUND)
        objs = objs.filter(activity=activity)

        locations = models_profile.VendorLocation.objects.all()

        subscription_end_date = request.user.vendor_subscription.end_date

        resp = serialize_location_slots(objs, locations, activity,subscription_end_date)

        return Response(resp)

    # @method_decorator(auth_decorators.only_vendor_allowed)
    def post(self, request, id):
        # objs = models.Slot.objects.all()
        try:
            activity = get_object_or_404(models.Activity, id=id)
            # pass
        except:
            return Response(responses.create_failure_response('activity object not found'), status=status.HTTP_404_NOT_FOUND)

        locations = request.data

        # print(objs)
        resp = []
        # print(locations)
        for location in locations:
            try:
                location_obj = models_profile.VendorLocation.objects.get(
                    shortname=location['location'])
            except:
                return Response(responses.create_failure_response('location ' + location['location'] + ' does not exists'), status=status.HTTP_400_BAD_REQUEST)

            # if(models.Slot.objects.filter(location=location_obj).exists()):
            #     return Response(responses.create_failure_response('location ' + location['location'] + ' already has some slots created. please make patch request to update'), status=status.HTTP_400_BAD_REQUEST)

            slots = location.pop("slots")
            # if(len(slots) > int(activity.noofsessions)):
            #     return Response(responses.create_failure_response("number of slots can't exceed maximum number of sessions specified in activity. please create slots less than or equal to maximum number of sessions specified in activity"), status=status.HTTP_400_BAD_REQUEST)

            for slot in slots:
                # slot["activity"] =
                slot["activity"] = activity.id
                slot["location"] = location_obj.id

            serializer = serializers_slots.SlotSerializer(
                data=slots, many=True)
            if (serializer.is_valid()):
                obj = serializer.save()
                # return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        loc_list = [l["location"] for l in locations]

        objs = models.Slot.objects.filter(
            activity=activity, location__shortname__in=loc_list)
        locations_qs = models_profile.VendorLocation.objects.filter(
            shortname__in=loc_list)
        resp = serialize_location_slots(objs, locations_qs, activity)

        return Response(resp)

    # @method_decorator(auth_decorators.only_vendor_allowed)
    def put(self, request, id):
        # objs = models.Slot.objects.all()
        try:
            activity = get_object_or_404(models.Activity, id=id)
            # pass
        except:
            return Response(responses.create_failure_response('activity object not found'), status=status.HTTP_404_NOT_FOUND)

        vs = request.user.vendor_subscription
        locations = request.data

        # print(objs)
        resp = []
        print("value is ", locations)
        for location in locations:
            try:
                location_obj = models_profile.VendorLocation.objects.filter(shortname=location['location'])
            except:
                return Response(responses.create_failure_response('location '+ ' does not exists'), status=status.HTTP_400_BAD_REQUEST)

            slots = location.pop("slots")
            # if(len(slots) > int(activity.noofsessions)):
            #     return Response(responses.create_failure_response("number of slots can't exceed maximum number of sessions specified in activity. please create slots less than or equal to maximum number of sessions specified in activity"), status=status.HTTP_400_BAD_REQUEST)

            for slot in slots:
                # slot["activity"] =
                slot["activity"] = activity.id
                slot["location"] = 1
                if("id" in slot):
                    # update
                    try:
                        obj = models.Slot.objects.get(id=int(slot["id"]))
                    except:
                        return Response(responses.create_failure_response("slot with id " + str(slot["id"]) + " does not exists"), status=status.HTTP_400_BAD_REQUEST)

                    serializer = serializers_slots.SlotSerializer(
                        obj, data=slot, many=False,context=request)
                    if (serializer.is_valid()):
                        obj = serializer.save()
                        # return Response(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                else:
                    # create
                    serializer = serializers_slots.SlotSerializer(
                        data=slot, many=False,context=request)
                    if (serializer.is_valid()):
                        obj = serializer.save()
                        # return Response(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        loc_list = [l["location"] for l in locations]
        objs = models.Slot.objects.filter(
            activity=activity, location__shortname__in=loc_list)
        locations_qs = models_profile.VendorLocation.objects.filter(
            shortname__in=loc_list)

        subscription_end_date = vs.end_date

        resp = serialize_location_slots(objs, locations_qs, activity,subscription_end_date)

        return Response(resp)
