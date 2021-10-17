from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('create-transaction/', views.createTransaction, name="createtransaction"),
    path('check-transaction/', views.checkTransaction, name="checktransaction"),
    path('payment-success/', views.paymentSuccess, name="paymentsuccess"),

    #---------
    path('create-order/', views.createOrder, name="createorder"),
]

