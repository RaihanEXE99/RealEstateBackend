from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, 
    AbstractBaseUser,
    PermissionsMixin
)
from django.contrib.auth import get_user_model

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
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

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
        return self.email
    
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
        return str(self.user.id)

class Organization(models.Model):
    name = models.CharField(max_length=100,default="anonymous")
    phone = models.CharField(max_length=16, null=True)
    email = models.EmailField(max_length=255, null=True)
    about = models.TextField(null=True)
    agents = models.ManyToManyField('Agent', blank=True,related_name='organizations_associated')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
class Agent(models.Model):
    name = models.CharField(max_length=60)
    phone = models.CharField(max_length=16, null=True)
    email = models.EmailField(max_length=255, null=True)
    about = models.TextField(null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name='agents_associated')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
class Invitation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f'Invitation to {self.organization} for {self.agent.email}'