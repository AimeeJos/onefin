from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """ manager for users."""

    def create_user(self, username, password):
        """ create save and return user"""
        if username is None:
            raise TypeError('Users should have a valid username!')
        if password is None:
            raise TypeError('Password should not be none!')
        # if phonenumber is None:
        #     raise TypeError('phonenumber should not be more than 12 digits!')

        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email=None,
                         is_active=None,
                         password=None):
        """ create and return new super user"""
        user = self.model(username=username,
                          email=email,                        
                          )

        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user

    

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    

    USERNAME_FIELD = 'username'

    objects = UserManager()

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        

