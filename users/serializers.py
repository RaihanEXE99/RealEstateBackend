from requests import Response
from rest_framework import serializers

from .models import Agent, UserProfile

class UserPhoneUpdateSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, max_length=15)

class MessageSerializer(serializers.Serializer):
    sender = serializers.IntegerField()
    recipient = serializers.IntegerField()
    message = serializers.CharField()
    # Add other fields as needed

    def to_representation(self, instance):
        return {
            'sender': instance.sender.id,
            'recipient': instance.recipient.id,
            'message': instance.message,
            # Add other fields as needed
        }
class UserAccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.CharField()
    # Add other fields as needed

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            # Add other fields as needed
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'number', 'skype_link', 'facebook_link', 'linkedin_link', 'title', 'email', 'website', 'twitter', 'pinterest', 'description']
# class ConversationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Conversation
#         fields = '__all__'
