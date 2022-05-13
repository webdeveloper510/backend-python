from rest_framework import serializers
from . import models


class AreaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = models.Area
        fields = ('id', 'name', 'status')

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Area name must be three or more charecters."
            )
        return value

    def create(self, validated_data):
        if ('id' in validated_data):
            id = validated_data.pop('id')  # Drop ID at object creation

        obj = super(AreaSerializer, self).create(validated_data)
        return obj

    def update(self, instance, validated_data):
        if ('id' in validated_data):
            id = validated_data.pop('id')  # Drop ID to prevent updation

        instance.save()
        super(AreaSerializer, self).update(instance, validated_data)
        return instance

class RegionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    areas = AreaSerializer(many=True, required=False)
    no_of_areas = serializers.SerializerMethodField()
    class Meta:
        model = models.Region
        fields = ('id', 'name', 'status','no_of_areas','areas')
    
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Region name must be three or more charecters."
            )
        return value

    def get_no_of_areas(self, obj):
        return obj.areas.count()

    def create(self, validated_data):
        if ('id' in validated_data):
            id = validated_data.pop('id')  # Drop ID at object creation
        areas = validated_data.pop('areas', [])
        
        instance = super(RegionSerializer, self).create(validated_data)
        
        for area in areas:
            # print(area)
            serializer = AreaSerializer(data=area, partial=True)
            if (serializer.is_valid()):
                obj = serializer.save()
                obj.region = instance
                obj.save()
            else:
                raise serializers.ValidationError({"error": serializer.errors})

        return instance

    def update(self, instance, validated_data):
        if ('id' in validated_data):
            id = validated_data.pop('id')  # Drop ID to prevent updation
        areas = validated_data.pop('areas', [])

        # print("got areas = ", areas)
        for area in areas:
            if ('id' in area):
                id = area.pop('id')
                try:
                    obj = instance.areas.get(id=id)
                except:
                    raise serializers.ValidationError({"error": "area with id " + str(id) + " does not exists"})
                serializer = AreaSerializer(obj, data=area, partial=True)
                if (serializer.is_valid()):
                    serializer.save()
                else:
                    raise serializers.ValidationError({"error": serializer.errors})
            else:  # create new object
                serializer = AreaSerializer(data=area, partial=True)
                if (serializer.is_valid()):
                    obj = serializer.save()
                    obj.region = instance
                    obj.save()
                else:
                    raise serializers.ValidationError({"error": serializer.errors})
                pass

        # instance.save()
        super(RegionSerializer, self).update(instance, validated_data)
        return instance

class CitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    regions = RegionSerializer(many=True, required=False)
    class Meta:
        model = models.City
        fields = ('id', 'name', 'status','regions')

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "City name must be three or more charecters."
            )
        return value

    def create(self, validated_data):
        if ('id' in validated_data):
            id = validated_data.pop('id')  # Drop ID at object creation
        regions = validated_data.pop('regions', [])
        
        instance = super(CitySerializer, self).create(validated_data)
        
        for region in regions:
            # print(regions)
            serializer = RegionSerializer(data=region, partial=True)
            if (serializer.is_valid()):
                obj = serializer.save()
                obj.city = instance
                obj.save()
            else:
                raise serializers.ValidationError({"error": serializer.errors})

        return instance

    def update(self, instance, validated_data):
        if ('id' in validated_data):
            id = validated_data.pop('id')  # Drop ID to prevent updation
        regions = validated_data.pop('regions', [])
        # print("got regions = ", regions)
        for region in regions:
            if ('id' in region):
                id = region.pop('id')
                try:
                    obj = instance.regions.get(id=id)
                except:
                    raise serializers.ValidationError({"error": "region with id " + str(id) + " does not exists"})
                serializer = RegionSerializer(obj, data=region, partial=True)
                if (serializer.is_valid()):
                    serializer.save()
                else:
                    raise serializers.ValidationError({"error": serializer.errors})
            else:  # create new object
                serializer = RegionSerializer(data=region, partial=True)
                if (serializer.is_valid()):
                    obj = serializer.save()
                    obj.city = instance
                    obj.save()
                else:
                    raise serializers.ValidationError({"error": serializer.errors})
                pass

        # instance.save()
        super(CitySerializer, self).update(instance, validated_data)
        return instance


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = ('display_character', 'name')


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, required=False)
    currency = CurrencySerializer()

    class Meta:
        model = models.Country
        fields = ('id', 'name', 'abbr',  'cities', 'currency')

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Country name must be three or more charecters.")
        return value

    def create(self, validated_data):
        cities = validated_data.pop('cities', [])
        currency = validated_data.pop('currency', None)

        instance = super(CountrySerializer, self).create(validated_data)

        for city in cities:
            # print(city)

            serializer = CitySerializer(data=city, partial=True)
            if (serializer.is_valid()):
                obj = serializer.save(country=instance)
                # obj.country = instance
                # obj.save()
            else:
                raise serializers.ValidationError({"error": serializer.errors})
            pass

        serializer = CurrencySerializer(data=currency, partial=True)
        if (serializer.is_valid()):
            obj = serializer.save(country=instance)
            # obj.country = instance
            # obj.save()
        else:
            raise serializers.ValidationError({"error": serializer.errors})
        pass

        return instance

    def update(self, instance, validated_data):
        cities = validated_data.pop('cities', [])
        currency = validated_data.pop('currency', None)

        for city in cities:
            if ('id' in city):
                id = city.pop('id')
                try:
                    obj = instance.cities.get(id=id)
                except:
                    raise serializers.ValidationError({"error": "city with id " + str(id) + " does not exists"})
                serializer = CitySerializer(obj, data=city, partial=True)
                if (serializer.is_valid()):
                    serializer.save()
                else:
                    raise serializers.ValidationError({"error": serializer.errors})
            else:  # create new object
                serializer = CitySerializer(data=city, partial=True)
                if (serializer.is_valid()):
                    obj = serializer.save(country=instance)
                    
                else:
                    raise serializers.ValidationError({"error": serializer.errors})
                pass
        # if(instance.currency.all().exists()):
        if (currency):
            if (models.Currency.objects.filter(country=instance).exists()):
                serializer = CurrencySerializer(instance.currency, data=currency, partial=True)
                if (serializer.is_valid()):
                    obj = serializer.save()
                    obj.country = instance
                    obj.save()
                else:
                    raise serializers.ValidationError({"error": serializer.errors})
                pass
            else:
                models.Currency.objects.create(country=instance, display_character=currency['display_character'],
                                               name=currency['name'])

        # instance.save(update_fields=["currency"])
        super(CountrySerializer, self).update(instance, validated_data)
        return instance


class AddressSerializer(serializers.ModelSerializer):
    # Used by Subscription Pricing
    class Meta:
        model = models.Address
        fields = ('address_line_1', 'address_line_2', 'phone_office',
                  'phone_mobile', 'zipcode')


# =========================================
# compact serializers to Filter for other modules
# =========================================


class RegionCompactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    # areas = AreaSerializer(many=True)
    no_of_areas = serializers.SerializerMethodField()
    class Meta:
        model = models.Region
        fields = ('id', 'name', 'status','no_of_areas')

    def get_no_of_areas(self, obj):
        return obj.areas.count()

class CityCompactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    # regions = RegionSerializer(many=True)
    class Meta:
        model = models.City
        fields = ('id', 'name', 'status')

class CountryCompactSerializer(serializers.ModelSerializer):
    # cities = CityCompactSerializer(many=True)
    currency = CurrencySerializer()
    class Meta:
        model = models.Country
        fields = ('id', 'name', 'abbr', 'currency')
    

# =========================================
# List serializers to Filter for other modules
# =========================================

class CountryListFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = ('id', 'name', 'abbr')

class CityListFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ('id', 'name', 'status')