from rest_framework.response import Response
from rest_framework import status
from agent.models import Agent
from django.contrib.auth import get_user_model
User= get_user_model()
from django.http import Http404

def countryAgentGuard(fn):
    def wrapper(self, request, format=None):
        if request.user.agent.country != "uk" or self.request.user.agent.agent_type == "local_agent":
            return Response({"message": "You Have no Permission."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return fn(self, request, format=None)
    return wrapper

def localAgentGuard(fn):
    def wrapper(self, request, format=None):
        if request.user.agent.agent_type == "local_agent":
            return Response({"message": "You Have no Permission."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return fn(self, request, format=None)
    return wrapper

def agentGuard(fn):
    def wrapper(self, request, pk):
        user = request.user
        try:
            agent = Agent.objects.get(pk=pk)
            if agent == user.agent:
                return fn(self, request, pk)
            if agent.agent_type == "country_agent" and user.agent.country=="uk" and user.agent.agent_type == "country_agent":
                return fn(self, request, pk)
            if agent.agent_type == "local_agent" and user.agent.agent_type =="country_agent" and agent.country == user.agent.country:
                return fn(self, request, pk)
            return Response({"message": "You Have no Permission."}, status=status.HTTP_403_FORBIDDEN) 
        except Agent.DoesNotExist:
            raise Http404
    return wrapper


def userGuard(fn):
    def wrapper(self, request, pk):
        r_user = request.user
        try:
            user = User.objects.get(pk=pk)
            if r_user.user_type == user.user_type and r_user.agent.country == user.agent.country:
                return fn(self, request, pk)
            else:
                return Response({"message": "You Have no Permission."}, status=status.HTTP_403_FORBIDDEN) 
        except User.DoesNotExist:
            raise Http404
    return wrapper