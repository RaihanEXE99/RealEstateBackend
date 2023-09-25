from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.permissions import AllowAny
from users.models import UserAccount as User

from rest_framework.permissions import IsAuthenticated
from .serializers import PasswordChangeSerializer
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .authentication import CustomJWTAuthentication
from rest_framework.authentication import TokenAuthentication

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from rest_framework import permissions

from django.http import JsonResponse
from .serializers import UserPhoneUpdateSerializer

class JWTCREATE(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

            response['return'] = {
                "type":"success"
            }
            return response

class JWTREFRESH(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response

class JWTVERIFY(TokenVerifyView):
    authentication_classes = [CustomJWTAuthentication]
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        if access_token:
            request.data['token'] = access_token
        response =  super().post(request, *args, **kwargs)
        return response

class JWTLOGOUT(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the old password is correct
            if not request.user.check_password(serializer.validated_data['old_password']):
                return Response({'detail': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's password
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()

            return Response({'detail': 'Password successfully changed.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserFullName(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        user = request.user
        full_name = user.full_name
        return Response({'full_name': full_name}, status=status.HTTP_200_OK)

class UpdateFullName(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            new_full_name = request.data.get('new_full_name')

            if new_full_name:
                user.full_name = new_full_name
                user.save()

                return Response({'message': 'Full name updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'New full name is required'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetUserFullName(APIView):
    authentication_classes = [CustomJWTAuthentication]

    def get(self, request):
        user = request.user
        full_name = user.full_name
        return Response({'full_name': full_name}, status=status.HTTP_200_OK)

class ChangePhoneNumberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Deserialize the request data
        serializer = UserPhoneUpdateSerializer(data=request.data)
        if serializer.is_valid():
            new_phone = serializer.validated_data['phone']

            # Get the authenticated user
            user = self.request.user

            # Update the user's phone number
            user.phone = new_phone
            user.save()

            return Response({"message": "Phone number updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
