from rest_framework.permissions import BasePermission
from agent.models import Agent
from django.http import Http404
from django.contrib.auth import get_user_model
User= get_user_model()
from payment.models import PaymentMethod, Deposit



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


class PaymentMethodPermission(BasePermission):
    def has_permission(self, request, view):
        r_user = request.user
        try:
            user = PaymentMethod.objects.get(pk=view.kwargs.get('pk'))
            if r_user.user_type == "country_user":
                return True
            else:
                return False
        except PaymentMethod.DoesNotExist:
            raise Http404


class DepositPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method =='GET':
            return True
        if request.method =='POST':
            user = request.user
            if request.data.get('agent'):
                try:
                    agent = Agent.objects.get(id=request.data['agent'])
                    if agent.agent_type == "local_agent":
                        if agent.country == request.user.agent.country:
                            request.data['status'] = "approved"
                            return True
                        else:
                            return False
                    else:
                        return False
                except:
                    raise Http404
            else:
                if request.user.user_type == "local_user":
                    request.data['agent'] = user.agent.id
                    request.data['status'] = "pending"
                    return True
                else:
                    return False

class DepositUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method =='GET':
            deposit = Deposit.objects.get(id=view.kwargs.get('pk'))
            if deposit.agent.country == request.user.agent.country and request.user.user_type == "country_user":
                return True
            if deposit.agent == request.user.agent:
                return True
            return False
        if request.method =='PATCH':
            user = request.user
            deposit = Deposit.objects.get(id=view.kwargs.get('pk'))
            if user.user_type == "country_user" and deposit.agent.country == request.user.agent.country:
                return True
            else:
                return False