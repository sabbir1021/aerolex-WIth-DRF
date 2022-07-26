from rest_framework import serializers
from django.contrib.auth import get_user_model
User= get_user_model()
from django.contrib.auth.hashers import make_password
from agent.models import Agent
from base.serializers import ReadWriteSerializerMethodField


class AgentLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id','name','email','phone_number']


class ProfileSerializer(serializers.ModelSerializer):
    agent = AgentLiteSerializer(read_only = True)
    class Meta:
        model = User
        fields = ['id','agent','username','email','first_name','phone_number','last_name','is_active',]

class UserSerializer(serializers.ModelSerializer):
    agent = ReadWriteSerializerMethodField()
    def get_agent(self, obj):
        return ProfileSerializer(obj.agent, many=False).data
    class Meta:
        model = User
        fields = ['id','agent','username','email','phone_number','first_name','last_name','password', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
    