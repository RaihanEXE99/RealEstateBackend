import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, 
    AbstractBaseUser,
    PermissionsMixin
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from base64 import b32encode
from hashlib import sha1
from random import random

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            **kwargs
        )
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        if user.role=="2":
            agent,create = Agent.objects.get_or_create(user__email=user.email)
            agent.user = user
            agent.save()
        elif user.role=="3":
            organization,create = Organization.objects.get_or_create(user__email=user.email)
            organization.user = user
            organization.save()
        profile,create = UserProfile.objects.get_or_create(user=user)
        profile.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


role_choice=(
    ('1','Normal User'),
    ('2','Agent'),
    ('3','Organization')
) 

class UserAccount(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=60, null=True)
    email = models.EmailField(unique=True, max_length=255)
    phone = models.CharField(max_length=16, null=True)
    role = models.CharField(
        max_length=15,
        choices=role_choice,
        default='1'
    )
    
    contact_email = models.EmailField(max_length=255, null=True)
    contact_phone = models.CharField(max_length=16, null=True)
    skype_url = models.URLField(max_length=200, null=True)
    facebook_url = models.URLField(max_length=200, null=True)
    website = models.URLField(max_length=200, null=True)
    description = models.TextField(null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name", "phone", "role"]

    def __str__(self):
        return self.email + " ->" + str(self.id)
    
class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=True,default="anonymous",null=True)
    number = models.CharField(max_length=20, blank=True,default="",null=True)
    skype_link = models.URLField(blank=True,default="",null=True)
    facebook_link = models.URLField(blank=True,default="",null=True)
    linkedin_link = models.URLField(blank=True,default="",null=True)
    title = models.CharField(max_length=255, blank=True,default="",null=True)
    email = models.EmailField(blank=True,default="",null=True)
    website = models.URLField(blank=True,default="",null=True)
    twitter = models.URLField(blank=True,default="",null=True)
    pinterest = models.URLField(blank=True,default="",null=True)
    description = models.TextField(blank=True,default="",null=True)

    def __str__(self):
        return str(self.user)

class Organization(models.Model):
    agents = models.ManyToManyField('Agent', blank=True,related_name='organizations_associated')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.user)
    
class Agent(models.Model):
    # organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name='agents_associated')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "User:"+str(self.user)+"---"+"Agent ID: "+str(self.id)

class Invitation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f'Invitation to {self.organization} for {self.agent.user.email} : {str(self.id)}'

class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('-date',)

    # function gets all messages between 'the' two users (requires your pk and the other user pk)
    def get_all_messages(id_1, id_2):
        messages = []
        # get messages between the two users, sort them by date(reverse) and add them to the list
        message1 = Message.objects.filter(sender_id=id_1, recipient_id=id_2).order_by('-date') # get messages from sender to recipient
        for x in range(len(message1)):
            messages.append(message1[x])
        message2 = Message.objects.filter(sender_id=id_2, recipient_id=id_1).order_by('-date') # get messages from recipient to sender
        for x in range(len(message2)):
            messages.append(message2[x])

        # because the function is called when viewing the chat, we'll return all messages as read
        for x in range(len(messages)):
            messages[x].is_read = True
        # sort the messages by date
        messages.sort(key=lambda x: x.date, reverse=False)
        return messages 
      
     # function gets all messages between 'any' two users (requires your pk)
    def get_message_list(u):
        # get all the messages
        m = []  # stores all messages sorted by latest first
        j = []  # stores all usernames from the messages above after removing duplicates
        k = []  # stores the latest message from the sorted usernames above
        for message in Message.objects.all():
            for_you = message.recipient == u  # messages received by the user
            from_you = message.sender == u  # messages sent by the user
            if for_you or from_you:
                m.append(message)
                m.sort(key=lambda x: x.sender.email)  # sort the messages by senders
                m.sort(key=lambda x: x.date, reverse=True)  # sort the messages by date

        # remove duplicates usernames and get single message(latest message) per username(other user) (between you and other user)
        for i in m:
            if i.sender.email not in j or i.recipient.email not in j:
                j.append(i.sender.email)
                j.append(i.recipient.email)
                k.append(i)

        return k
# class Conversation(models.Model):
#     participants = models.ManyToManyField(get_user_model(), related_name='conversations')
#     created_at = models.DateTimeField(auto_now_add=True)
#     def clean(self):
#         if self.participants.count() != 2:
#             raise ValidationError("A conversation must have exactly two participants.")
#         super().clean()
        
# class Message(models.Model):
#     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
#     text = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)