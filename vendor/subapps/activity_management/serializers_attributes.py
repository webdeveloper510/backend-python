from rest_framework import serializers
from . import models

class SubAttributeSerializer(serializers.ModelSerializer):
    deleteable = serializers.SerializerMethodField()
    attributeGroup = serializers.CharField(source='attribute.name')

    def get_deleteable(self,obj):
        if obj.attribute.activityAttr.all().count() > 0 :
            return False
        return True
    
    class Meta:
        model = models.SubAttribute
        fields = ('id','attributeGroup','name','deleteable')


    

class AttributeSerializer(serializers.ModelSerializer):

    subAttribute = SubAttributeSerializer(many=True, required=False)

    class Meta:
        model = models.Attribute
        fields = ('id', 'name', 'subAttribute',)

    def create(self, validated_data):
        print("validates data is", validated_data)
        queryset = models.Attribute.objects.all()
        subattributes = validated_data.pop('subAttribute', None )
        instance = super(AttributeSerializer, self).create(validated_data)
        if(subattributes != None):
            for subatt in subattributes:
                subAttSerializer = SubAttributeSerializer(data=subatt)
                if(subAttSerializer.is_valid()):
                    subAttSerializer.save(attribute=instance)
                else:
                    print(subAttSerializer.errors)
        return instance

    def update(self, instance, validated_data):
        subattributes = validated_data.pop('subAttribute', None )

        for attr,value in validated_data.items():
            setattr(instance,attr,value)    

        if subattributes is not None:
            instance.subAttribute.all().delete()
            for subatt in subattributes:
                serializer = SubAttributeSerializer(data=subatt)
                if serializer.is_valid():
                    serializer.save(attribute=instance)

        instance = super(AttributeSerializer, self).update(instance, validated_data)
        return instance

