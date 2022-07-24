from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
User= get_user_model
from base.models import USER_ROLE_CHOICES, USER_TYPE_CHOICES , USER_STATUS_CHOICES

# Create your models here.

class User(AbstractUser):
    # username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length = 10)
    user_role = models.CharField(max_length=20,choices=USER_ROLE_CHOICES)
    user_type = models.CharField(max_length=20,choices=USER_TYPE_CHOICES)
    status = models.CharField(max_length=20,choices=USER_STATUS_CHOICES)
#     REQUIRED_FIELDS = ['username','phone_number', 'user_role', 'user_type', 'status']
#     USERNAME_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



class Agent(models.Model):
    name = models.CharField(max_length = 70)
    phone_number = models.CharField(max_length = 20)
    country = models.CharField(max_length = 70)
    email = models.CharField(max_length = 70)
    address = models.CharField(max_length = 70)
    currency = models.CharField(max_length = 70)
    unique_identifier = models.CharField(max_length = 70)
    payment_policy = models.CharField(max_length = 70)
    payment_policy = models.CharField(max_length = 70)


    def __str__(self):
        return self.name
    
    
    