from django.db import models
from django.forms import URLField
from agent.models import Agent
from base.models import PAYMENT_TYPE_CHOICES, DEPOSIT_STATUS_CHOICES

# Create your models here.

class PaymentMethod(models.Model):
    account_name = models.CharField(max_length = 150)
    account_number = models.CharField(max_length = 150, unique=True)
    payment_type = models.CharField(max_length=20,choices=PAYMENT_TYPE_CHOICES)
    agent = models.ForeignKey(Agent,  on_delete=models.CASCADE)
    is_active = models.BooleanField()

    def __str__(self):
        return self.account_name

class Deposit(models.Model):
    payment_method = models.ForeignKey(PaymentMethod,  on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now=False, auto_now_add=False)
    attachment_url = models.URLField(max_length=200,blank=True, null=True)
    amount = models.IntegerField()
    agent = models.ForeignKey(Agent,  on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices=DEPOSIT_STATUS_CHOICES)

    def __str__(self):
        return self.agent.name

    
class DepositHistory(models.Model):
    deposit = models.ForeignKey(Deposit,  on_delete=models.CASCADE, related_name='deposit_history')
    status_name = models.CharField(max_length=20,choices=DEPOSIT_STATUS_CHOICES)
    date_time = models.DateTimeField()

    def __str__(self):
        return str(self.deposit.amount)

    