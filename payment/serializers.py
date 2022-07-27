from rest_framework import serializers
from django.contrib.auth import get_user_model
User= get_user_model()
from .models import PaymentMethod

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id','account_name','account_number','agent','is_active']
