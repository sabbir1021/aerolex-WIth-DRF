from requests import request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User= get_user_model()
from .serializers import AgentSerializer
from accounts.serializers import UserSerializer
from django.http import Http404
from .models import Agent

# Create your views here.

class CountryAgent(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        if request.user.agent.country != "uk" or request.user.agent.agent_type != "country_agent":
             return Response({"message": "You Have no Permission."}, status=status.HTTP_400_BAD_REQUEST)
        
        agents = Agent.objects.filter(agent_type="country_agent")
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.agent.country != "uk" or request.user.agent.agent_type != "country_agent":
            return Response({"message":"you have not permission for create Country Agent"}, status=status.HTTP_400_BAD_REQUEST)
        country = request.data['country']
        agent_check = Agent.objects.filter(country=country)
        if agent_check:
            return Response({"message": "This Country Agent already Exsist."}, status=status.HTTP_400_BAD_REQUEST)
        request.data["agent_type"] = "country_agent"
        # request.data["balance"] = 0
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocalAgent(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        if request.user.agent.agent_type != "country_agent":
             return Response({"message": "You Have no Permission."}, status=status.HTTP_400_BAD_REQUEST)
        agents = Agent.objects.filter(agent_type="local_agent", country=request.user.agent.country)
        serializer = AgentSerializer(agents, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.agent.agent_type == "local_agent":
            return Response({"message":"you have not permission for create Country Agent"}, status=status.HTTP_400_BAD_REQUEST)
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


class AgentSingle(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            agent = Agent.objects.get(pk=pk)
            if self.request.user.agent.id == agent.id:
                return agent
            if self.request.user.agent.country == "uk" or self.request.user.agent.agent_type == "country_agent":
                if agent.agent_type == "country_agent":
                    return agent
            if self.request.user.agent.agent_type == "country_agent" and agent.agent_type == "local_agent":
                return agent
            
            raise Http404
        except Agent.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AgentSerializer(snippet)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AgentSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountSetup(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Agent.objects.get(pk=pk)
        except Agent.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        snippet = self.get_object(pk)
        if snippet.signup_confirmation:
            return Response({"message": "Already signup complete."}, status=status.HTTP_400_BAD_REQUEST)
        request.data['email'] = snippet.email
        request.data['phone_number'] = snippet.phone_number
        request.data['user_type'] = "country_user" if snippet.agent_type == "country_agent" else "local_user"
        request.data['agent'] = snippet.id
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            snippet.signup_confirmation = True
            snippet.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)