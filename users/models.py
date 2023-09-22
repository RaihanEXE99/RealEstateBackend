from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, 
    AbstractBaseUser,
    PermissionsMixin
)


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

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )

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