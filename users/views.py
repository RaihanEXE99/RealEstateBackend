import json
from django.forms import model_to_dict
from django.http import JsonResponse
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .models import Agent,Message, Invitation, Organization, UserProfile,UserAccount

from .serializers import MessageSerializer, UserAccountSerializer, UserPhoneUpdateSerializer, UserProfileSerializer
import re

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny 

from django.shortcuts import get_object_or_404

from django.core.serializers import serialize

class JWTCREATE(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response

class JWTREFRESH(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)
        return response

class JWTVERIFY(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response

class JWTLOGOUT(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
    
class ChangePasswordView(APIView):
    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        re_new_password = request.data.get('re_new_password')

        if len(new_password) < 8:
            return Response({'detail': 'New password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != re_new_password:
            return Response({'detail': 'New password and confirmation do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.check_password(old_password):
            return Response({'detail': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()

        return Response({'detail': 'Password successfully changed.'}, status=status.HTTP_200_OK)

class GetUserFullName(APIView):
    def get(self, request):
        user = request.user
        full_name = user.full_name
        return Response({'full_name': full_name}, status=status.HTTP_200_OK)

class GetUserMe(APIView):
    def get(self, request):
        user = request.user
        full_name = user.full_name
        return Response({'full_name': full_name,'email':user.email}, status=status.HTTP_200_OK)

class UpdateFullName(APIView):
    def post(self, request):
        try:
            user = request.user
            new_full_name = request.data.get('new_full_name')

            if new_full_name:
                # Check if the full name contains only letters and spaces
                if re.match("^[a-zA-Z\s]+$", new_full_name):
                    # Remove leading and trailing spaces from the full name
                    new_full_name = new_full_name.strip()
                    
                    user.full_name = new_full_name
                    user.save()
                    return Response({'message': 'Full name updated successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Full name contains numbers or special characters'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'New full name is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetUserFullName(APIView):
    def get(self, request):
        user = request.user
        full_name = user.full_name
        return Response({'full_name': full_name}, status=status.HTTP_200_OK)

class ChangePhoneNumberView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserPhoneUpdateSerializer(data=request.data)
        if serializer.is_valid():
            new_phone = serializer.validated_data['phone']

            user = self.request.user

            user.phone = new_phone
            user.save()

            return Response({"message": "Phone number updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(APIView):
    def get(self, request):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)

        return Response({
            "name": profile.name,
            "number": profile.number,
            "skype_link": profile.skype_link,
            "facebook_link": profile.facebook_link,
            "linkedin_link": profile.linkedin_link,
            "title": profile.title,
            "email": profile.email,
            "website": profile.website,
            "twitter": profile.twitter,
            "pinterest": profile.pinterest,
            "description": profile.description,
        },status=status.HTTP_200_OK)
    
class UserProfileCreateUpdateView(APIView):
    def post(self, request):
        data = request.data
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
        profile.name = data.get("name", profile.name)
        profile.number = data.get("number", profile.number)
        profile.skype_link = data.get("skype_link", profile.skype_link)
        profile.facebook_link = data.get("facebook_link", profile.facebook_link)
        profile.linkedin_link = data.get("linkedin_link", profile.linkedin_link)
        profile.title = data.get("title", profile.title)
        profile.email = data.get("email", profile.email)
        profile.website = data.get("website", profile.website)
        profile.twitter = data.get("twitter", profile.twitter)
        profile.pinterest = data.get("pinterest", profile.pinterest)
        profile.description = data.get("description", profile.description)

        profile.save()

        return Response({"message": "User profile created/updated successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def autocomplete_agent_emails(request):
    if request.GET.get('q'):
        query = request.GET['q']
        # agents = Agent.objects.filter(user__email__icontains=query).values_list('user__email','user__full_name', flat=True)
        agents = Agent.objects.filter(user__email__icontains=query)
        alist = []
        for agent in agents:
            alist.append({
                "name":agent.user.full_name,
                "email":agent.user.email,
            })
        return JsonResponse(alist, safe=False)
    return JsonResponse([], safe=False)

class AddAgentToOrganizationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:

            auser = Agent.objects.get(user__email=email)
            organization = Organization.objects.get(user=request.user)
            
            # Check if there's an existing invitation for the same organization and email
            invitation = Invitation.objects.filter(organization=organization, agent=auser, is_accepted=False, is_rejected=False).first()
            if invitation:
                return Response({'message': f'An invitation to {auser.user.email} already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not auser in organization.agents.all():
                # Create a new invitation
                invitation = Invitation(organization=organization, agent=auser)
                invitation.save()
                return Response({'message': f'Invitation sent to {auser.user.email}'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': f'{auser.user.email} is already associated with an organization'}, status=status.HTTP_400_BAD_REQUEST)
        except Agent.DoesNotExist:
            return Response({'message': f'User with email {email} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class ListInvitationsView(APIView):
    def get(self, request):
        try:
            that_agent = Agent.objects.get(user=request.user)
            invitations = Invitation.objects.filter(agent=that_agent, is_rejected=False,is_accepted=False)
        except Agent.DoesNotExist:
            return JsonResponse({"error": "Agent does not exist"}, status=status.HTTP_404_NOT_FOUND)
        invitation_list = []
        for invitation in invitations:
            organizationProfile = UserProfile.objects.get(user=invitation.organization.user)
            invitation_data = {
                "id":invitation.id,
                "organization": organizationProfile.name,
                "agent_email": invitation.agent.user.email
            }
            invitation_list.append(invitation_data)

        return JsonResponse(invitation_list, safe=False)

class AcceptInvitationView(APIView):
    def post(self, request, invitation_id):
        try:
            agent = Agent.objects.get(user=request.user)
            invitation = Invitation.objects.get(agent=agent,id=invitation_id, is_accepted=False, is_rejected=False)
        except Invitation.DoesNotExist:
            return JsonResponse({"error": "Invitation does not exist or has already been accepted/rejected"}, status=status.HTTP_404_NOT_FOUND)

        # Perform the action to accept the invitation (e.g., set is_accepted to True).
        invitation.is_accepted = True
        invitation.save()

        organization = Organization.objects.get(user=invitation.organization.user)
        organization.agents.add(invitation.agent)

        organization.save()

        return JsonResponse({"message": "Invitation accepted"}, status=status.HTTP_200_OK)

class RejectInvitationView(APIView):
    def post(self, request, invitation_id):
        try:
            invitation = Invitation.objects.get(id=invitation_id, is_accepted=False, is_rejected=False)
        except Invitation.DoesNotExist:
            return JsonResponse({"error": "Invitation does not exist or has already been accepted/rejected"}, status=status.HTTP_404_NOT_FOUND)

        # Perform the action to reject the invitation (e.g., set is_rejected to True).
        invitation.is_rejected = True
        invitation.save()

        try:
            organization = Organization.objects.get(user=invitation.organization.user)
            organization.agents.remove(invitation.agent)
            organization.save()
        except:
            return JsonResponse({"message": "Invitation rejected."}, status=status.HTTP_200_OK)

        return JsonResponse({"message": "Invitation rejected"}, status=status.HTTP_200_OK)
    
class AgentListView(APIView):
    def get(self, request):
        user = request.user
        # Retrieve all agents from the database
        organization = Organization.objects.get(user=user)
        agents = organization.agents.all()

        ag = []
        for agent in agents:
            profile = UserProfile.objects.get(id=agent.user.id)
            print(profile)
            serializer  = UserProfileSerializer(profile)
            ag.append(serializer.data)

        # Return the list of agents as a JSON response
        return Response(ag)

class RemoveAgentFromOrganization(APIView):
    def post(self, request, id):
        try:
            organization = get_object_or_404(Organization, user__id=request.user.id)
            agent = get_object_or_404(Agent, user__id=id)

            organization.agents.remove(agent)
            organization.save()

            return Response({"data":"Agent removed from the organization."})
        except:
            return Response({"data":"Something went wrong!"})

class MessagesListView(APIView):
    def get(self, request):
        user = UserAccount.objects.get(pk=request.user.pk)  # get your primary key
        messages = Message.get_message_list(user) # get all messages between you and the other user

        other_users = [] # list of other users

        # getting the other person's name fromthe message list and adding them to a list
        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)
                
        mserializer = MessageSerializer(messages, many=True)
        userializer = UserAccountSerializer(other_users,many=True)
        context= {}
        context['messages_list'] = mserializer.data
        context['other_users'] = userializer.data
        context['you'] = user.email
        print(context)
        return Response(context)

class UserListsView(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(UserAccount, pk=request.user.pk)
        users = UserAccount.objects.exclude(pk=user.pk)

        user_data = []  # List to store user data
        for u in users:
            user_data.append({
                'id': u.id,
                'email': u.email,
                'full_name':u.full_name
                # Add other fields as needed
            })

        return Response({'users': user_data}, status=status.HTTP_200_OK)
    
class InboxView(APIView):

    def get(self, request, id, *args, **kwargs):
        user = get_object_or_404(UserAccount, id=id)
        current_user = get_object_or_404(UserAccount, pk=request.user.pk)
        messages = Message.get_all_messages(current_user, user)

        message_data = []

        for message in messages:
            message_data.append({
                "id":message.id,
                'sender_id': message.sender.id,
                'recipient_id': message.recipient.id,
                'sender': message.sender.full_name,
                'recipient':message.recipient.full_name,
                'message': message.message,
                'timestamp': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                # Add other message-related fields as needed
            })

        return Response({'messages': message_data}, status=status.HTTP_200_OK)

    def post(self, request, id, *args, **kwargs):
        current_user = get_object_or_404(UserAccount, pk=request.user.pk)
        recipient = get_object_or_404(UserAccount, id=id)
        message_text = request.data.get('message')

        if not request.user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        if message_text and request.method == 'POST':
            message = Message.objects.create(sender=current_user, recipient=recipient, message=message_text)
            message_data = {
                'sender_id': message.sender.id,
                'recipient_id': message.recipient.id,
                'sender': message.sender.full_name,
                'recipient':message.recipient.full_name,
                'message': message.message,
                'timestamp': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                # 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                # Add other message-related fields as needed
            }
            return Response({'message': message_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid message data'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny]) # Any user can view (FOR PUBLIC URLS)
def getAgentProfile(request,id, *args, **kwargs):
    try:
        Agent.objects.get(user__id=id)
        profile = UserProfile.objects.get(user__id=id)
        # Serialize the UserProfile instance to JSON
        serialized_data = serialize('json', [profile, ])

        # Convert serialized data to Python dictionary
        deserialized_data = json.loads(serialized_data)

        # Extract the fields you need or return the entire data
        user_profile_data = deserialized_data[0]['fields']
        user_profile_data['user']=id

        # Return the serialized data in JSON format
        return JsonResponse(user_profile_data)
    except Exception as error:
        print(error)
        return Response({"error":"Invalid ID/Something wrong happend!"})

@api_view(['GET'])
@permission_classes([AllowAny]) # Any user can view (FOR PUBLIC URLS)
def getOrganizationProfile(request,id, *args, **kwargs):
    try:
        Organization.objects.get(user__id=id)
        profile = UserProfile.objects.get(user__id=id)
        # Serialize the UserProfile instance to JSON
        serialized_data = serialize('json', [profile, ])

        # Convert serialized data to Python dictionary
        deserialized_data = json.loads(serialized_data)

        # Extract the fields you need or return the entire data
        user_profile_data = deserialized_data[0]['fields']
        user_profile_data['user']=id

        # Return the serialized data in JSON format
        return JsonResponse(user_profile_data)
    except Exception as error:
        print(error)
        return Response({"error":"Invalid ID/Something wrong happend!"})

# class ConversationView(APIView):
#     def get(self, request, *args, **kwargs):
#         receiver_email = request.query_params['q']
#         receiver = UserAccount.objects.filter(email=receiver_email).first()
#         if not receiver:
#             return Response({"detail": "Receiver not found."}, status=status.HTTP_400_BAD_REQUEST)

#         user = request.user

#         if(receiver_email==user.email):return Response({"error":"Can't send text to your self!"})
#         # Check if a conversation exists between the user and the receiver
#         conversation = Conversation.objects.filter(participants=user).filter(participants=receiver).first()

#         if not conversation:
#             # If no conversation exists, create a new one
#             conversation = Conversation.objects.create()
#             conversation.participants.add(user, receiver)
#             conversation.save()

#         messages = Message.objects.filter(conversation=conversation)
#         for msg in messages:
#             print(msg)
#         return Response({
#             "id":conversation.id,
#             "msg":[msg.sender.email+":"+msg.text for msg in messages]
#         })

# class SendMessageView(APIView):
#     def post(self, request):
#         sender = request.user
#         receiver_email = request.data.get('receiver_email')
#         text = request.data.get('text')
#         if(receiver_email==sender.email):return Response({"error":"Can't send text to your self!"})

#         # Find the receiver by email
#         receiver = UserAccount.objects.filter(email=receiver_email).first()
#         if not receiver:
#             return Response({"detail": "Receiver not found."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Check if a conversation exists between the sender and receiver
#         conversation = Conversation.objects.filter(participants=sender).filter(participants=receiver).first()
        
#         if len(conversation.participants.all())==1:return Response({"error":"Can't send text to your self!"})

#         if not conversation:
#             # If no conversation exists, create a new one
#             conversation = Conversation.objects.create()
#             conversation.participants.add(sender, receiver)

#         # Create a new message in the conversation
#         if len(conversation.participants.all())==1:return Response({"error":"Can't send text to your self!"})
#         message = Message.objects.create(conversation=conversation, sender=sender, text=text)

#         return Response({"detail": "Message sent successfully."}, status=status.HTTP_201_CREATED)
    
# class ConversationListView(APIView):
#     def get(self, request):
#         # Ensure the user is authenticated
#         if not request.user.is_authenticated:
#             return Response({"detail": "Authentication required."}, status=status.HTTP_403_FORBIDDEN)

#         # Retrieve all conversations where the user is a participant
#         user = request.user
#         conversations = Conversation.objects.filter(participants=user)

#         # Prepare a list of conversation data
#         conversation_data = []
#         for conversation in conversations:
#             participants = [participant.email for participant in conversation.participants.all()]
#             conversation_data.append({
#                 "id": conversation.id,
#                 "participants": participants,
#                 "created_at": conversation.created_at,
#             })

#         return Response(conversation_data)
    
# def initAgent(request):
#     user = request.user
#     if user.role == "2":
#         agent,create = Agent.objects.get_or_create(user__email=user.email)
#         agent.user = user
#         agent.save()
#         return True
#     else:
#         return False
# def initOrganization(request):
#     user = request.user
#     if user.role == "3":
#         organization,create = Organization.objects.get_or_create(user__email=user.email)
#         organization.user = user
#         organization.save()
#         return True
#     else:
#         return Response("Invalid Request!(Its not an Organization Account)",status=status.HTTP_400_CREATED)
# class OrganizationBasicView(APIView):
#     def get(self, request):
#         user = request.user
#         if user.role=="3":
#             print("Organization")
#             criteria = {
#                 'user': user,  # Replace with the desired name
#             }
#             organization, created = Organization.objects.get_or_create(**criteria)
#             userPorfile = UserProfile.objects.get(user=user)
#             return Response({
#                 "name":organization.name,
#                 "number":userPorfile.number,
#                 "email":userPorfile.email,
#                 "about":userPorfile.about,
#             }, status=status.HTTP_200_OK)

#         else:
#             print("Not Organization Account")
#             return Response({"message": "Invalid Request"}, status=status.HTTP_404_NOT_FOUND)
        
# class OrganizationProfileUpdate(APIView):
#     def post(self, request):
#         user = request.user
#         if user.role=="3":
#             organization = Organization.objects.get(user=user)
#             data = request.data
#             organization.name = data.get("name", organization.name)
#             organization.email = data.get("email", organization.email)
#             organization.phone = data.get("phone", organization.phone)
#             organization.about = data.get("description", organization.about)
#             organization.save()
            
#             return Response({
#                 "name":organization.name,
#                 "phone":organization.phone,
#                 "email":organization.email,
#                 "about":organization.about,
#             }, status=status.HTTP_200_OK)

#         else:
#             print("Not Organization Account")
#             return Response({"message": "Invalid Request"}, status=status.HTTP_404_NOT_FOUND)


# #AGENT
# class AgentBasicView(APIView):
#     def get(self, request):
#         user = request.user
#         if user.role=="2":
#             print("Agent")
#             criteria = {
#                 'user': user,  # Replace with the desired name
#             }
#             agent, created = Agent.objects.get_or_create(**criteria)
#             return Response({
#                 "name":agent.name,
#                 "phone":agent.phone,
#                 "email":agent.email,
#                 "about":agent.about,
#             }, status=status.HTTP_200_OK)

#         else:
#             print("Not Agent Account")
#             return Response({"message": "Invalid Request"}, status=status.HTTP_404_NOT_FOUND)
        
# class AgentProfileUpdate(APIView):
#     def post(self, request):
#         user = request.user
#         if user.role=="2":
#             agent = Agent.objects.get(user=user)
#             data = request.data
#             agent.name = data.get("name", agent.name)
#             agent.email = data.get("email", agent.email)
#             agent.phone = data.get("phone", agent.phone)
#             agent.about = data.get("about", agent.about)
#             agent.save()
            
#             return Response({
#                 "name":agent.name,
#                 "phone":agent.phone,
#                 "email":agent.email,
#                 "about":agent.about,
#             }, status=status.HTTP_200_OK)

#         else:
#             print("Not Agent Account")
#             return Response({"message": "Invalid Request"}, status=status.HTTP_404_NOT_FOUND)

def getAgents(request, *args, **kwargs):
    if request.method == 'Get':
        id = request.GET.get('id')
        organization = UserAccount.objects.get(id=id)
        agents = UserAccount.objects.filter(role='2')
        
        names = [agent.full_name for agent in agents]

        data = {
            'titles': names
        }

        return JsonResponse(data)