from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('change_password/', views.ChangePassword.as_view(), name="change_password"),
    path('profile_update/', views.ProfileUpdate.as_view(), name="profile_update"),
    path('user/', views.UserCreate.as_view(), name="user"),
    path('user/<int:pk>', views.UserSingle.as_view(), name="user_get"),


    
]