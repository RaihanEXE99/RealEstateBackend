from requests import Response
from rest_framework import serializers

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    re_new_password = serializers.CharField(required=True)

    def validate(self, data):
        new_password = data.get('new_password')
        re_new_password = data.get('re_new_password')

        if len(new_password) < 8:
            raise serializers.ValidationError("New password must be at least 8 characters long.")
            # raise Response("New password must be at least 8 characters long.")

        if new_password != re_new_password:
            raise serializers.ValidationError("New password and confirmation do not match.")

        return data

class UserPhoneUpdateSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, max_length=15)