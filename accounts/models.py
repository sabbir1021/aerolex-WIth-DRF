from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
User= get_user_model
from base.models import USER_ROLE_CHOICES, USER_TYPE_CHOICES , USER_STATUS_CHOICES
from agent.models import Agent
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Enter an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.status = 'active'
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length = 20, unique=True)
    user_role = models.CharField(max_length=20,choices=USER_ROLE_CHOICES)
    user_type = models.CharField(max_length=20,choices=USER_TYPE_CHOICES)
    status = models.CharField(max_length=20,choices=USER_STATUS_CHOICES)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()





    
    
    