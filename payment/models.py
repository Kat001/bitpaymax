from django.db import models
from django.db.models import CASCADE

# Create your models here.

class ExchangeRates(models.Model):
    """
    This model will be used to keep update of exchanges rates..
    """
    usdAmount = models.FloatField(default=0)
    trxAmount = models.FloatField(default=0)
    ethAmount = models.FloatField(default=0)
    btcAmount = models.FloatField(default=0)
    
    def __str__(self):
        return "Exchange Rates"

class Payment(models.Model):
    """
    This model will store ..
    """
    paymentType =(
        ('INR', "Indian Rupees"),
        ('TRX', "Tron Currency"),
        ('ETH', "Etherium Currency"),
        ('BTC', "Bitcoin Currency")
    )
    user = models.ForeignKey("account.Account", on_delete=CASCADE, related_name="payment_user")
    currency = models.CharField(choices=paymentType, max_length=10)
    address = models.CharField(default="", max_length=50)
    txId = models.CharField(default="", max_length=50)
    status = models.BooleanField(default=False)
    dollarAmount = models.FloatField(default=0)
    cryptoPayment = models.FloatField(default=0)
    createdOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return user.username
