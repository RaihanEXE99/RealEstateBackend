from requests import Response
from rest_framework import serializers

class UserPhoneUpdateSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, max_length=15)