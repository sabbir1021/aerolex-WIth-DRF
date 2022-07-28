from django.urls import path
from . import views

app_name = "settings"

urlpatterns = [
    path('file-upload/', views.FileUploadCreate.as_view(), name="file_upload"),
    path('markup-setting/', views.MarkupSettingCreateList.as_view(), name="markup_setting"),
    path('file-upload/', views.FileUploadCreate.as_view(), name="file_upload"),
]