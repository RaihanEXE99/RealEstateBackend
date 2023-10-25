from django.urls import path, re_path
from .views import (
    JWTCREATE,
    JWTREFRESH,
    JWTVERIFY,
    JWTLOGOUT,

    ChangePasswordView,
    GetUserFullName,

    UpdateFullName,
    ChangePhoneNumberView,
    GetUserMe,

    UserProfileDetailView,
    UserProfileCreateUpdateView
)

urlpatterns = [
    path('jwt/create/', JWTCREATE.as_view()),
    path('jwt/refresh/', JWTREFRESH.as_view()),
    path('jwt/verify/', JWTVERIFY.as_view()),
    path('logout/', JWTLOGOUT.as_view()),

    path('change-password/', ChangePasswordView.as_view()),
    path('change-phone/', ChangePhoneNumberView.as_view()),
    path('user/get_full_name/', GetUserFullName.as_view()),
    path('user/update_full_name/', UpdateFullName.as_view()),
    path('user/getUserMe/', GetUserMe.as_view()),

    path('profiles/<int:pk>/', UserProfileDetailView, name='profileDetail'),
    path('profile/update/', UserProfileCreateUpdateView.as_view(), name='profileUpdate'),
    
]