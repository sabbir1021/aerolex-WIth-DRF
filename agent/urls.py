from django.urls import path
from . import views

app_name = "agent"

urlpatterns = [
    path('country-agents/', views.CountryAgent.as_view(), name="country_agent"),
    path('local-agents/', views.LocalAgent.as_view(), name="local_agent"),

   
]