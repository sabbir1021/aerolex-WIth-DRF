from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User= get_user_model()
from .models import FileUpload, MarkupSetting
from .serializers import FileUploadSerializer, MarkupSettingSerializer, CurrencySettingSerializer
from base.permission import MarkupSettingUpdatePermission
# Create your views here.

class MarkupSettingCreateList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        markup_settings = MarkupSetting.objects.filter()
        serializer = MarkupSettingSerializer(markup_settings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MarkupSettingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarkupSettingUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        snippet = MarkupSetting.objects.get(pk=pk)
        serializer = MarkupSettingSerializer(snippet)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        snippet = MarkupSetting.objects.get(pk=pk)
        serializer = MarkupSettingSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FileUploadCreate(APIView):
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "successfully uploaded."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)