from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('payment-method/', views.PaymentMethodListCreate.as_view(), name="payments_method"),
    path('payment-method/<int:pk>', views.PaymentMethodViewUpdate.as_view(), name="payments_method_update"),
    path('deposit/', views.DepositListCreate.as_view(), name="deposit"),
    path('deposit/<int:pk>', views.DepositViewUpdate.as_view(), name="deposit_update"),

]