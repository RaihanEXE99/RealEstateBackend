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
    UserProfileCreateUpdateView,

    OrganizationBasicView,
    OrganizationProfileUpdate,

    AgentBasicView,
    AgentProfileUpdate,

    AddAgentToOrganizationView,
    autocomplete_agent_emails,

    ListInvitationsView,
    AcceptInvitationView,
    RejectInvitationView,
    AgentListView
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

    path('profile/details/', UserProfileDetailView.as_view(), name='profileDetail'),
    path('profile/update/', UserProfileCreateUpdateView.as_view(), name='profileUpdate'),

    path('organization/profile/', OrganizationBasicView.as_view(), name='OrganizationBasicView'),
    path('organization/profile/update/', OrganizationProfileUpdate.as_view(), name='OrganizationProfileUpdate'),
    path('agent/profile/', AgentBasicView.as_view(), name='AgentBasicView'),
    path('agent/profile/update/', AgentProfileUpdate.as_view(), name='AgentProfileUpdate'),
    path('addAgent/', AddAgentToOrganizationView.as_view(), name='AddAgentToOrganizationView'),
    path('autocomplete_agent_emails/', autocomplete_agent_emails, name='autocomplete_agent_emails'),

    path('invitations/', ListInvitationsView.as_view(), name='list_invitations'),
    path('invitation/<int:invitation_id>/accept/', AcceptInvitationView.as_view(), name='accept-invitation'),
    path('invitation/<int:invitation_id>/reject/', RejectInvitationView.as_view(), name='reject-invitation'),

    path('myAgents/', AgentListView.as_view(), name='agent_list'),

]