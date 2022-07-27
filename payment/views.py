from wsgiref.util import request_uri
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User= get_user_model()
from .serializers import PaymentMethodSerializer, DepositSerializer
from django.http import Http404
from payment.models import PaymentMethod, Deposit, DepositHistory
from base.permission import PaymentMethodPermission, DepositPermission, DepositUpdatePermission
from datetime import datetime
from agent.models import Agent
# Create your views here.

class PaymentMethodListCreate(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        payment_method = PaymentMethod.objects.filter(is_active=True, agent__country=request.user.agent.country)
        serializer = PaymentMethodSerializer(payment_method, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.user_type == "local_user":
            return Response({"message": "You have no Permission"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PaymentMethodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentMethodViewUpdate(APIView):
    permission_classes = [IsAuthenticated,PaymentMethodPermission]
    def get(self, request, pk):
        snippet = PaymentMethod.objects.get(pk=pk)
        serializer = PaymentMethodSerializer(snippet)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        snippet = PaymentMethod.objects.get(pk=pk)
        serializer = PaymentMethodSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositListCreate(APIView):
    permission_classes = [IsAuthenticated, DepositPermission]
    def get(self, request, format=None):
        deposits = Deposit.objects.all()
        serializer = DepositSerializer(deposits, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            DepositHistory.objects.create(deposit=obj,status_name=request.data['status'],date_time=datetime.now())
            if request.data['status'] == "approved":
                agent = Agent.objects.get(id=request.data['agent'])
                print(agent.balance,request.data['amount'])
                agent.balance = (0 if agent.balance == None else agent.balance) + request.data['amount']
                agent.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositViewUpdate(APIView):
    permission_classes = [IsAuthenticated, DepositUpdatePermission]
    def get(self, request, pk):
        snippet = Deposit.objects.get(pk=pk)
        serializer = DepositSerializer(snippet)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        snippet = Deposit.objects.get(pk=pk)
        status = request.data['status']
        previous_status = snippet.status
        serializer = DepositSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            DepositHistory.objects.create(deposit=snippet,status_name=status,date_time=datetime.now())
            if previous_status != "approved" and status == "approved":
                agent = snippet.agent
                agent.balance = (0 if agent.balance == None else agent.balance) + snippet.amount
                agent.save()
            if previous_status == "approved" and status == "rejected":
                agent = snippet.agent
                agent.balance = (0 if agent.balance == None else agent.balance) - snippet.amount
                agent.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)