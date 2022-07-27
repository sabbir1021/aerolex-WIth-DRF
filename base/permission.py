from rest_framework.permissions import BasePermission
from agent.models import Agent
from django.http import Http404
from django.contrib.auth import get_user_model
User= get_user_model()


class CountryAgentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.agent.country != "uk" or request.user.agent.agent_type == "local_agent":
            return False
        else:
            return True

class LocalAgentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.agent.agent_type == "local_agent":
            return False
        else:
            return True

class AgentPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            agent = Agent.objects.get(pk=view.kwargs.get('pk'))
            if agent == user.agent:
                return True
            if agent.agent_type == "country_agent" and user.agent.country=="uk" and user.agent.agent_type == "country_agent":
                return True
            if agent.agent_type == "local_agent" and user.agent.agent_type =="country_agent" and agent.country == user.agent.country:
                return True
        except Agent.DoesNotExist:
            raise Http404
        
class UserPermission(BasePermission):
    def has_permission(self, request, view):
        r_user = request.user
        try:
            user = User.objects.get(pk=view.kwargs.get('pk'))
            if r_user.user_type == user.user_type and r_user.agent.country == user.agent.country:
                return True
            else:
                return False
        except User.DoesNotExist:
            raise Http404