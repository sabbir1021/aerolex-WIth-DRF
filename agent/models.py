from django.db import models
from django.contrib.auth import get_user_model
User= get_user_model
from base.models import COUNTRY_CHOICES, PAYMENT_POLICY_CHOICES, AGENT_TYPE_CHOICES
# Create your models here.

class Agent(models.Model):
    name = models.CharField(max_length = 70)
    phone_number = models.CharField(max_length = 20)
    country =  models.CharField(max_length=20,choices=COUNTRY_CHOICES)
    email = models.CharField(max_length = 70)
    address = models.CharField(max_length = 70)
    currency = models.CharField(max_length = 70)
    unique_identifier = models.CharField(max_length = 70)
    payment_policy =  models.CharField(max_length=20,choices=PAYMENT_POLICY_CHOICES)
    agent_type = models.CharField(max_length=20,choices=AGENT_TYPE_CHOICES)

    def __str__(self):
        return self.name