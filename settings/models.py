from platform import platform
from django.db import models
from agent.models import Agent
from base.models import MARKUP_TYPE_CHOICES , PLATFORM_CHOICES, COUNTRY_CHOICES
# Create your models here.

class MarkupSetting(models.Model):
    platform =  models.CharField(max_length=20,choices=PLATFORM_CHOICES)
    name = models.CharField(max_length=50)
    markup_amount = models.IntegerField()
    markup_type = models.CharField(max_length=20,choices=MARKUP_TYPE_CHOICES)
    applicable_for = models.ForeignKey(Agent, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)

    class Meta:
        unique_together = ('name', 'applicable_for',)

    def __str__(self):
        return self.name

class CurrencySetting(models.Model):
    country = models.CharField(max_length=20,choices=COUNTRY_CHOICES)
    rate = models.IntegerField()
    applicable_for = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class CurrencySettingHistory(models.Model):
    currency_setting = models.ForeignKey(CurrencySetting, on_delete=models.CASCADE)
    country = models.CharField(max_length=20,choices=COUNTRY_CHOICES)
    current_rate = models.IntegerField()
    current_start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    previous_rate = models.IntegerField(blank=True,null=True)
    previous_start_date = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.currency_setting.country


class FileUpload(models.Model):
    file_name = models.FileField(upload_to="ok")

    def __str__(self):
        return str(self.file_name)
    
    