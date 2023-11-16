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

    # OrganizationBasicView,
    # OrganizationProfileUpdate,

    # AgentBasicView,
    # AgentProfileUpdate,

    AddAgentToOrganizationView,
    autocomplete_agent_emails,

    ListInvitationsView,
    AcceptInvitationView,
    RejectInvitationView,
    AgentListView,

    # ConversationView,
    # ConversationListView,
    # SendMessageView,

    MessagesListView,
    UserListsView,
    InboxView,

    getAgentProfile,
    getOrganizationProfile,
    RemoveAgentFromOrganization,
    
    UserProfilePictureUpdateView,
    agentDetails
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

    path('addAgent/', AddAgentToOrganizationView.as_view(), name='AddAgentToOrganizationView'),
    path('removeAgent/<int:id>/', RemoveAgentFromOrganization.as_view(), name='RemoveAgentFromOrganization'),
    path('autocomplete_agent_emails/', autocomplete_agent_emails, name='autocomplete_agent_emails'),

    path('invitations/', ListInvitationsView.as_view(), name='list_invitations'),
    path('invitation/<int:invitation_id>/accept/', AcceptInvitationView.as_view(), name='accept-invitation'),
    path('invitation/<int:invitation_id>/reject/', RejectInvitationView.as_view(), name='reject-invitation'),

    path('myAgents/', AgentListView.as_view(), name='agent_list'),

    path('messageList/', MessagesListView.as_view(), name='message_list'),
    path('meet/', UserListsView.as_view(), name='users_list'),

    # path('conversation/', ConversationView.as_view(), name='conversation-view'),
    # path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    # path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('inbox/<str:id>/', InboxView.as_view(), name='inbox'),
    path('getAgentProfile/<int:id>',getAgentProfile,name="getAgentProfile"),
    path('getOrganizationProfile/<int:id>',getOrganizationProfile,name="getOrganizationProfile"),

    path('update-profile-picture/', UserProfilePictureUpdateView.as_view(), name='update_profile_picture'),
    path('agentDetails/<str:id>/', agentDetails, name='agentDetails'),
]