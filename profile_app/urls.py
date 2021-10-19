from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name="profile"),
    # Profile related paths.....
    path('personal-info/', views.personalInfo, name="personalinfo"),
    path('update-profile/', views.updateProfile, name="updateprofile"),
    path('change-password/', views.changePassword, name="changepassword"),
    path('change-txn-password/', views.changeTxnPassword, name="changetxnpassword"),

    # Id related paths......
    path('add-fund/', views.addFund, name="addfund"),
    path('activate-id/', views.activateId, name="activateid"),
    path('my-packs/', views.myPacks, name="mypacks"),
    path('activate-id/<str:amount>', views.activateIdAmount, name="activateidamount"),
    path('transfer-fund/', views.transferFund, name="transferfund"),
    path('transfer-fund-history/', views.transferFundHistory, name="transferfundhistory"),

    # Team related paths.....
    path('referral-team/<int:user_id>', views.referralTeam, name="referralteam"),
    path('level-team/', views.levelTeam, name="levelteam"),
    path('level-team2/', views.levelTeam2, name="levelteam2"),
    path('level-team3/', views.levelTeam3, name="levelteam3"),
    path('level-team4/', views.levelTeam4, name="levelteam4"),
    path('level-team5/', views.levelTeam5, name="levelteam5"),

    # Income Related paths......
    path('level-income/', views.levelIncome, name="levelincome"),
    path('roi-income/', views.roiIncome, name="roiincome"),

    # Withdrawal related paths.....
    path('admin-withdrawal/', views.adminWithdrawal, name="adminwithdrawal"),
    path('admin-withdrawal/accept/<int:iid>', views.adminWithdrawalAccept, name="adminwithdrawalaccept"),
    path('admin-withdrawal/cancel/<int:iid>', views.adminWithdrawalCancel, name="adminwithdrawalcancel"),
    
    
    path('withdrawal/', views.withdrawal, name="withdrawal"),
    path('withdrawal-history/', views.withdrawalHistory, name="withdrawalhistory"),

    # Support related paths.....
    path('support-ticket/', views.supportTicket, name="supportticket"),
    path('support-ticket-history/', views.supportTicketHistory, name="supporttickethistory"),

]
