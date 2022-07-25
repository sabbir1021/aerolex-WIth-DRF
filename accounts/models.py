from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
User= get_user_model
from base.models import USER_ROLE_CHOICES, USER_TYPE_CHOICES , USER_STATUS_CHOICES
from agent.models import Agent
# Create your models here.

class User(AbstractUser):
    # username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length = 10)
    user_role = models.CharField(max_length=20,choices=USER_ROLE_CHOICES)
    user_type = models.CharField(max_length=20,choices=USER_TYPE_CHOICES)
    status = models.CharField(max_length=20,choices=USER_STATUS_CHOICES)
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE)
#     REQUIRED_FIELDS = ['username','phone_number', 'user_role', 'user_type', 'status']
#     USERNAME_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    
    
    