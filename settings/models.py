from platform import platform
from django.db import models
from agent.models import Agent
from base.models import MARKUP_TYPE_CHOICES , PLATFORM_CHOICES
# Create your models here.

class MarkupSetting(models.Model):
    platform =  models.CharField(max_length=20,choices=PLATFORM_CHOICES)
    name = models.CharField(max_length=50)
    markup_amount = models.IntegerField()
    markup_type = models.CharField(max_length=20,choices=MARKUP_TYPE_CHOICES)
    applicable_for = models.ForeignKey(Agent, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    