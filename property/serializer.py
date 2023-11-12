import json
from rest_framework import serializers
from .models import Property, Address, PropertyDetails

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
    
class PropertySerializer(serializers.ModelSerializer):
    address = NoValidationField()
    details = NoValidationField()
    class Meta:
        model = Property
        fields = '__all__'
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        details_data = validated_data.pop('details')

        address = Address.objects.create(**address_data)
        details = PropertyDetails.objects.create(**details_data)
        property = Property.objects.create(address=address,details=details, **validated_data)
        return property
    
    #  address_obj, created = Address.objects.create(
    #             house=address_data['house'],
    #             street=address_data['street'],
    #             city=address_data['city'],
    #             state=address_data['state'],
    #             country=address_data['country'],
    #             zip=address_data['zip']
    #         )
    #     details_obj, created = PropertyDetails.objects.create(
    #             cid=details_data['cid'],
    #             size_unit=details_data['size_unit'],
    #             size=details_data['size'],
    #             rooms=details_data['rooms'],
    #             bed=details_data['bed'],
    #             bath=details_data['bath'],
    #             floor=details_data['floor'],
    #             built=details_data['built'],
    #             structure=details_data['structure'],
    #             garages=details_data['garages'],
    #             garage_size=details_data['garage_size'],
    #         )
# class PropertySerializer(serializers.ModelSerializer):
#     # address = AddressSerializer()
#     details = PropertyDetailsSerializer()

#     class Meta:
#         model = Property
#         fields = '__all__'

#     def create(self, validated_data):
#         address_data = validated_data.pop('address')
#         details_data = validated_data.pop('details')
#         address_obj = Address.objects.create(
#                 house=address_data['house'],
#                 street=address_data['street'],
#                 city=address_data['city'],
#                 state=address_data['state'],
#                 country=address_data['country'],
#                 zip=address_data['zip']
#             )
#         details = PropertyDetails.objects.create(**details_data)

#         # address = Address.objects.create(address_obj.pk)
#         property = Property.objects.create(address=address_obj, details=details, **validated_data)
#         return property