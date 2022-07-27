from operator import truediv
import re
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User= get_user_model()
from .serializers import PaymentMethodSerializer
from accounts.serializers import UserSerializer
from django.http import Http404
from payment.models import PaymentMethod
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