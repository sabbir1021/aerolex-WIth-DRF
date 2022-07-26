from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User= get_user_model()
from .serializers import AgentSerializer
from django.http import Http404
from .models import Agent
# Create your views here.

class CountryAgent(APIView):
    def get(self, request, format=None):
        agents = Agent.objects.filter(agent_type="country_agent")
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        country = request.data['country']
        agent_check = Agent.objects.filter(country=country)
        if agent_check:
            return Response({"message": "This Country Agent already Exsist."}, status=status.HTTP_400_BAD_REQUEST)
        request.data["agent_type"] = "country_agent"
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocalAgent(APIView):
    def get(self, request, format=None):
        agents = Agent.objects.filter(agent_type="local_agent")
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        country = request.user.agent.country
        currency = request.user.agent.currency
        payment_policy = request.user.agent.payment_policy
        request.data["country"] = country
        request.data["currency"] = currency
        request.data["payment_policy"] = payment_policy
        request.data["agent_type"] = "local_agent"
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)