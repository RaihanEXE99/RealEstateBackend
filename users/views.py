from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .serializers import PasswordChangeSerializer

from .serializers import UserPhoneUpdateSerializer

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
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(serializer.validated_data['old_password']):
                return Response({'detail': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)

            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()

            return Response({'detail': 'Password successfully changed.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserFullName(APIView):
    def get(self, request):
        user = request.user
        full_name = user.full_name
        return Response({'full_name': full_name}, status=status.HTTP_200_OK)

class UpdateFullName(APIView):
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
