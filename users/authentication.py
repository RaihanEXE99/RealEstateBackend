from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpRequest

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            header = self.get_header(request)

            if header is None:
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
            else:
                raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token
        except:
            return None
        
# class CustomTokenAuthentication(TokenAuthentication):
#     def authenticate(self, request):
#         if request.method == 'POST':
#             # Get the access token from the cookie for POST requests
#             access_token = request.COOKIES.get('access_token')

#             if not access_token:
#                 return None

#             # Verify the token and return the user
#             return self.authenticate_credentials(access_token)

#         # For other HTTP methods, use the default TokenAuthentication behavior
#         return super().authenticate(request)