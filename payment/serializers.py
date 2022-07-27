from rest_framework import serializers
from django.contrib.auth import get_user_model
User= get_user_model()
from .models import PaymentMethod, Deposit, DepositHistory

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id','account_name','account_number','agent','is_active']


class DepositHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositHistory
        fields = ['id','status_name','date_time']

class DepositSerializer(serializers.ModelSerializer):
    histroy = DepositHistorySerializer(source='deposit_history',many=True,read_only=True)
    class Meta:
        model = Deposit
        fields = ['id','payment_method','issue_date','attachment_url','amount','agent','status','histroy']