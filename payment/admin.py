from django.contrib import admin
from .models import PaymentMethod, Deposit , DepositHistory
# Register your models here.

admin.site.register(PaymentMethod)
admin.site.register(Deposit)
admin.site.register(DepositHistory)