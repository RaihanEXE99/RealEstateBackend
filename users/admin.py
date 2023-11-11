from django.contrib import admin
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import *

user=get_user_model()

admin.site.register(user)
# admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(Agent)
admin.site.register(Invitation)
admin.site.register(Message)

from django.contrib.contenttypes.models import ContentType
admin.site.register(ContentType)
