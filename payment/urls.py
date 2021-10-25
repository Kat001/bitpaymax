from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('create-transaction/', views.createTransaction, name="createtransaction"),
    path('check-transaction/', views.checkTransaction, name="checktransaction"),
    path('payment-success/', views.paymentSuccess, name="paymentsuccess"),

    #Webhook ....
    path('payment-callback/',views.PaymentCallback.as_view(), name="paymentcallback"),

    path('payout/',views.payout, name="payout"),


]

