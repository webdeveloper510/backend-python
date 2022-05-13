from rest_framework import serializers
from django.db.models import Max
from . import models


class SubCategorySerializer(serializers.ModelSerializer):
    deleteable = serializers.SerializerMethodField()

    def get_deleteable(self,obj):
        if obj.activities.all().count() > 0:
            return False
        return True
    class Meta:
        model = models.SubCategory
        fields = ('id','name','deleteable')

class WeightageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    weightage = serializers.IntegerField()
class UpdateWeightageSerializer(serializers.Serializer):
    weightage_list = WeightageSerializer(many=True)

    def create(self,data):
        wlist = data.pop('weightage_list')

        for w in wlist:
            id = w.pop("id")
            weightage = w.pop("weightage")
            models.Category.objects.filter(id=id).update(weightage=weightage)
        return wlist


class CategorySerializer(serializers.ModelSerializer):
    subCategory = SubCategorySerializer(many=True, required=False)

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'subCategory','weightage')
        extra_kwargs={"weightage":{"required":False}}

    def create(self, validated_data):
        print("validates data is", validated_data)
        queryset = models.Category.objects.all()
        subcategories = validated_data.pop('subCategory', None)
        weightage = models.Category.objects.aggregate(Max('weightage'))
        weightage = weightage['weightage__max'] 
        if weightage == None:
            weightage = 0 
        validated_data['weightage'] =  weightage + 1
        instance = super(CategorySerializer, self).create(validated_data)
        if subcategories != None:
            for subatt in subcategories:
                subAttSerializer = SubCategorySerializer(data=subatt)
                if subAttSerializer.is_valid():
                    subAttSerializer.save(category=instance)
                else:
                    print(subAttSerializer.errors)
        return instance

    def update(self, instance, validated_data):
        subcategories = validated_data.pop('subCategory',None)
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        
        instance.save()

        if subcategories is not None:
            instance.subCategory.all().delete()
            for subatt in subcategories:
                serializer = SubCategorySerializer(data=subatt)
                if serializer.is_valid():
                    models.SubCategory.objects.create(category=instance,**subatt)

        #instance = super(CategorySerializer, self).update(instance, validated_data)
        
        return instance

