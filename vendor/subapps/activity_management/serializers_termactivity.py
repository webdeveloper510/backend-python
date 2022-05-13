import string

from rest_framework import serializers, fields
from .models import TermActivity, TermActivitySlot
import random


class TermactivityslotSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermActivitySlot
        fields = ('slot', 'slotdate', 'sttime','edtime', 'sessionid')

class TermactivitySerializer(serializers.ModelSerializer):
    term_slot = TermactivityslotSerializer(many=True)
    class Meta:
        model = TermActivity
        fields = ('id','activity','location','name', 'classid', 'publishdate','commencementdate','totalenrolled','totalavailable','term_slot','price')

    def create(self, validated_data):
        print('validated data is', validated_data)
        term_data = validated_data.pop('term_slot')
        classid = validated_data.pop('classid')
        newclassid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        print('newclassid is', newclassid)
        term = TermActivity.objects.create(**validated_data,classid=newclassid)
        for data in term_data:
            print("data is ", data)
            data['sessionid'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
            TermActivitySlot.objects.create(slot=term, **data)
        return term

    def update(self, instance, validated_data):
        term_data = validated_data.pop('term_slot')
        slots = instance.term_slot.all()
        slots = list(slots)
        instance.id = validated_data.get('id', instance.id)
        instance.activity = validated_data.get('activity', instance.activity)
        instance.location = validated_data.get('location', instance.location)
        instance.name = validated_data.get('name', instance.name)
        instance.classid = validated_data.get('classid', instance.classid)
        instance.publishdate = validated_data.get('publishdate', instance.publishdate)
        instance.commencementdate = validated_data.get('commencementdate', instance.commencementdate)
        instance.totalenrolled = validated_data.get('totalenrolled', instance.totalenrolled)
        instance.totalavailable = validated_data.get('totalavailable', instance.totalavailable)
        instance.price = validated_data.get('price', instance.price)

        for data in term_data:
            d1 = slots.pop(0)
            d1.slotdate = data.get('slotdate', d1.slotdate)
            d1.sttime = data.get('sttime',d1.sttime)
            d1.edtime = data.get('edtime',d1.edtime)
            d1.save()

        instance.save()
        return instance
