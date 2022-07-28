from rest_framework import serializers
from .models import FileUpload, MarkupSetting, CurrencySetting

class MarkupSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkupSetting
        fields = ['id','platform','name','markup_amount','markup_type','applicable_for','country']

class CurrencySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencySetting
        fields = ['id','country','rate','applicable_for']

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['file_name']
