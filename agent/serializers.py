from rest_framework import serializers
from django.contrib.auth import get_user_model
User= get_user_model()
from .models import Agent

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id','name','phone_number','country','email','address','currency','unique_identifier','payment_policy','agent_type']
