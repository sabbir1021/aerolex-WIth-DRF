from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
User= get_user_model()
from payment.models import PaymentMethod, Deposit
from agent.models import Agent
from django.shortcuts import get_object_or_404


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
        agent = get_object_or_404(Agent, pk=view.kwargs.get('pk'))
        if agent == user.agent:
            return True
        if agent.agent_type == "country_agent" and user.agent.country=="uk" and user.agent.agent_type == "country_agent":
            return True
        if agent.agent_type == "local_agent" and user.agent.agent_type =="country_agent" and agent.country == user.agent.country:
            return True
        
        
class UserPermission(BasePermission):
    def has_permission(self, request, view):
        r_user = request.user
        user = get_object_or_404(User,pk=view.kwargs.get('pk'))
        if r_user.user_type == user.user_type and r_user.agent.country == user.agent.country:
            return True
        else:
            return False
       


class PaymentMethodPermission(BasePermission):
    def has_permission(self, request, view):
        r_user = request.user
        payment_method = get_object_or_404(PaymentMethod,pk=view.kwargs.get('pk'))
        if r_user.user_type == "country_user":
            return True
        else:
            return False
        


class DepositPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method =='GET':
            return True
        if request.method =='POST':
            user = request.user
            if request.data.get('agent'):
                agent = get_object_or_404(Agent,id=request.data['agent'])
                if agent.agent_type == "local_agent":
                    if agent.country == request.user.agent.country:
                        request.data['status'] = "approved"
                        return True
                    else:
                        return False
                else:
                    return False
               
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
            deposit = get_object_or_404(Deposit,id=view.kwargs.get('pk'))
            if deposit.agent.country == request.user.agent.country and request.user.user_type == "country_user":
                return True
            if deposit.agent == request.user.agent:
                return True
            return False
            
        if request.method =='PATCH':
            user = request.user
            deposit = get_object_or_404(Deposit,id=view.kwargs.get('pk'))
            if user.user_type == "country_user" and deposit.agent.country == request.user.agent.country:
                return True
            else:
                return False
            

# Settings

class MarkupSettingUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.agent.agent_type == "local_agent":
            return False
        else:
            return True