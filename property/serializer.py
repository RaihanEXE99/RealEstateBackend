import json
from rest_framework import serializers
from .models import Property, Address, PropertyDetails, Image, Video
from django.db import transaction

from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['property', 'image']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class PropertyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDetails
        fields = '__all__'

class NoValidationField(serializers.CharField):  # Example: Use CharField for 'address'
    def to_internal_value(self, data):
        return data 
    
# class PropertySerializer(serializers.ModelSerializer):
#     address = NoValidationField()
#     details = NoValidationField()
#     class Meta:
#         model = Property
#         fields = '__all__'
#     def create(self, validated_data):
#         with transaction.atomic():
#             address_data = validated_data.pop('address')
#             details_data = validated_data.pop('details')

#             address = Address.objects.create(**address_data)
#             details = PropertyDetails.objects.create(**details_data)

#             property = Property.objects.create(address=address, details=details, **validated_data)
#             return property

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

# class PropertySerializer(serializers.ModelSerializer):
#     address = NoValidationField()
#     details = NoValidationField()
#     video = NoValidationField()
#     images = NoValidationField()

#     class Meta:
#         model = Property
#         fields = '__all__'

#     def create(self, validated_data):
#         address_data = validated_data.pop('address')
#         details_data = validated_data.pop('details')
#         images_data = validated_data.pop('images')
#         video_file  = validated_data.pop('video')

#         address = Address.objects.create(**address_data)
#         details = PropertyDetails.objects.create(**details_data)
#         # video = Video.objects.create(**video_data)
#         # images = Video.objects.create(**images_data)
#         video = Video.objects.create(video=video_file)

#         # images = validated_data.FILES.getlist('images')

        

#         property_instance = Property.objects.create(
#             address=address,
#             details=details,
#             video=video,
#             **validated_data
#         )

#         for image_item in images_data:
#             image = Image.objects.create(image=image_item)
#             property_instance.images.add(image)
#         # for image in images:
#         #     # Process or save the image to your model or filesystem
#         #     image_obj = Image.objects.create(image=image)
#         #     property_instance.images.add(image_obj)

#         # property_instance.video = video  # Assign the video to the property instance
#         property_instance.save()

#         return property_instance
class PropertySerializer(serializers.ModelSerializer):
    address = NoValidationField()
    details = NoValidationField()
    video = NoValidationField()
    images = serializers.ListField(child=serializers.FileField(), write_only=True)
    

    class Meta:
        model = Property
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        details_data = validated_data.pop('details')
        images_data = validated_data.pop('images')
        video_file  = validated_data.pop('video')

        address = Address.objects.create(**address_data)
        details = PropertyDetails.objects.create(**details_data)

        video = Video.objects.create(video=video_file)

        property_instance = Property.objects.create(
            address=address,
            details=details,
            video=video,
            **validated_data
        )

        for image_item in images_data:
            image = Image.objects.create(image=image_item)
            property_instance.images.add(image)
        property_instance.save()

        return property_instance
    

# Serializer for Property
class PropertySerializerAll(serializers.ModelSerializer):
    address = AddressSerializer()
    details = PropertyDetailsSerializer()

    class Meta:
        model = Property
        fields = '__all__'