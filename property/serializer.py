from rest_framework import serializers
from .models import Property, Address, PropertyDetails, Image, Video
from django.db import transaction

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class PropertyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDetails
        fields = '__all__'

# class PropertySerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    details = PropertyDetailsSerializer()

    class Meta:
        model = Property
        fields = '__all__'

    def create(self, validated_data):
        with transaction.atomic():
            address_data = validated_data.pop('address')
            details_data = validated_data.pop('details')

            address = Address.objects.create(**address_data)
            details = PropertyDetails.objects.create(**details_data)

            property = Property.objects.create(address=address, details=details, **validated_data)
            return property
class PropertySerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    details = PropertyDetailsSerializer()
    
    class Meta:
        model = Property
        fields = ['title', 'price', 'price_unit', 'price_type', 'thumbnail', 
                  'property_category', 'property_status', 'post_type', 'loc', 'lat', 'long',
                  'date', 'desc', 'address', 'details', 'hide_contact', 'user']

    def create(self, validated_data):
        with transaction.atomic():
            address_data = validated_data.pop('address')
            details_data = validated_data.pop('details')
            address = Address.objects.create(**address_data)
            details = PropertyDetails.objects.create(**details_data)

            property_instance = Property.objects.create(
                address=address, 
                details=details, 
                **validated_data
            )
            return property_instance
        

from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['property', 'image']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['property', 'video']