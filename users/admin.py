from django.contrib import admin
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import *

user=get_user_model()

admin.site.register(user)
# admin.site.register(UserAccount)
# admin.site.register(UserAccountManager)