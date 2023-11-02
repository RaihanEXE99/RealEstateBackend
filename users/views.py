from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .models import Organization, UserProfile,UserAccount

from .serializers import UserPhoneUpdateSerializer
import re

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny 

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
        

@api_view(['GET'])
@permission_classes([AllowAny]) # Any user can view (FOR PUBLIC URLS)
def UserProfileDetailView(request, pk):
    try:
        user = UserAccount.objects.filter(id=pk).first()
        if user is None:
            # If the UserAccount doesn't exist, return an error response
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
        profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            profile.name = ""
            profile.number = ""
            profile.skype_link = ""
            profile.facebook_link = ""
            profile.linkedin_link = ""
            profile.title = ""
            profile.email = ""
            profile.website = ""
            profile.twitter = ""
            profile.pinterest = ""
            profile.description = ""
            profile.save()
        
        data = {
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
        }
        return Response(data, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
class UserProfileCreateUpdateView(APIView):
    def post(self, request):
        data = request.data
        try:
            profile = UserProfile.objects.get(pk=request.user.id)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
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
    

class OrganizationBasicView(APIView):
    def get(self, request):
        user = request.user
        if user.role=="3":
            print("Organization")
            criteria = {
                'user': user,  # Replace with the desired name
            }
            organization, created = Organization.objects.get_or_create(**criteria)
            return Response({
                "name":organization.name,
                "phone":organization.phone,
                "email":organization.email,
                "about_organization":organization.about_organization,
            }, status=status.HTTP_200_OK)

        else:
            print("Not Organization Account")
            return Response({"message": "Invalid Request"}, status=status.HTTP_404_NOT_FOUND)
        
class OrganizationBasicView(APIView):
    def get(self, request):
        user = request.user
        if user.role=="3":
            print("Organization")
            criteria = {
                'user': user,  # Replace with the desired name
            }
            organization, created = Organization.objects.get_or_create(**criteria)
            return Response({
                "name":organization.name,
                "phone":organization.phone,
                "email":organization.email,
                "about_organization":organization.about_organization,
            }, status=status.HTTP_200_OK)

        else:
            print("Not Organization Account")
            return Response({"message": "Invalid Request"}, status=status.HTTP_404_NOT_FOUND)

# class UserProfileCreateUpdateView(APIView):
#     def post(self, request):
#         data = request.data
#         try:
#             profile = UserProfile.objects.get(pk=request.user.id)
#         except UserProfile.DoesNotExist:
#             return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
#         profile.name = data.get("name", profile.name)
#         profile.number = data.get("number", profile.number)
#         profile.skype_link = data.get("skype_link", profile.skype_link)
#         profile.facebook_link = data.get("facebook_link", profile.facebook_link)
#         profile.linkedin_link = data.get("linkedin_link", profile.linkedin_link)
#         profile.title = data.get("title", profile.title)
#         profile.email = data.get("email", profile.email)
#         profile.website = data.get("website", profile.website)
#         profile.twitter = data.get("twitter", profile.twitter)
#         profile.pinterest = data.get("pinterest", profile.pinterest)
#         profile.description = data.get("description", profile.description)

#         profile.save()

#         return Response({"message": "User profile created/updated successfully"}, status=status.HTTP_201_CREATED)