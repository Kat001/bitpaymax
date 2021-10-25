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
    mtx = models.CharField(max_length=200,default="")

    def __str__(self):
        return self.user.username


class Bank_Info(models.Model):
	user = models.OneToOneField("account.Account", on_delete=models.CASCADE)
	account_holder_name = models.CharField(max_length=40,default="")
	account_number = models.CharField(max_length=30,default='')
	branch_name = models.CharField(max_length=40,default='')
	ifsc_code = models.CharField(max_length=20,default="")
	bank_name = models.CharField(max_length=30,default='')
	nominee_name = models.CharField(max_length=30,default="")
	cheak = models.BooleanField(default=False)

	@property
	def username(self):
		return self.user.username


	def __str__(self):
		return(f'{self.user.username}')
