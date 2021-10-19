from django.db import models
from django.db.models import CASCADE
# Create your models here.

class Package(models.Model):
    amount = models.PositiveIntegerField(default=0)
    days = models.PositiveIntegerField(default=0)
    max_profit = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.amount)

class Fund(models.Model):
    user = models.OneToOneField("account.Account",on_delete=models.CASCADE)
    available_fund = models.PositiveIntegerField(default=0)
    previoud_fund = models.PositiveIntegerField(default=0)
    system_added = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Do your Cutomizatons here...
        if self.system_added:
            amount = self.available_fund-self.previoud_fund
            record = Fundrecord(fundType="ADD",user=self.user,amount=amount)
            self.previoud_fund = self.available_fund
            self.system_added = False
        super(Fund, self).save(*args, **kwargs)

    # def save(self, toUser=None):
    #     if toUser is None:
    #         amount = self.available_fund-self.previoud_fund
    #         record = Fundrecord(fundType="ADD",user=self.user,amount=amount)
    #         self.previoud_fund = self.available_fund

    #         record.save()
    #     super(Fund, self).save()

    def __str__(self):
        return self.user.username

class Fundrecord(models.Model):

    fundRecordTypeChoices = (
        ('TFS', 'Transfer'),
        ('ADD', 'Added From System'),
    )

    fundType = models.CharField(max_length=17, choices=fundRecordTypeChoices,default="ADD")
    user = models.ForeignKey("account.Account", on_delete=CASCADE, related_name="sender_user")
    to_user = models.ForeignKey("account.Account", on_delete=CASCADE, null=True, blank=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField(default=0)

    
    def __str__(self):
        return self.user.username

class Roiincome(models.Model):
    user  = models.ForeignKey("account.Account", on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    createdOn = models.DateTimeField(auto_now_add=True)
    income = models.FloatField(default=0)

    def __str__(self):
        return self.user.username + ' ' + str(self.package.amount)

class LevelIncome(models.Model):
    user 	    = models.ForeignKey("account.Account", on_delete=models.CASCADE)
    from_user 	= models.ForeignKey("account.Account",on_delete=models.CASCADE,related_name="activated_iid")
    date 	    = models.DateField(auto_now_add=True)
    level       = models.CharField(max_length=10,default="")
    income 	    = models.FloatField(default=0)

    def __str__(self):
        return self.user.username

class Withdrawal(models.Model):
    """
    This model will store ..
    """
    withdrawType =(
        ('INR', "Indian Rupees"),
        ('TRX', "Tron Currency"),
        ('ETH', "Etherium Currency"),
        ('BTC', "Bitcoin Currency")
    )
    user = models.ForeignKey("account.Account", on_delete=CASCADE, related_name="withdraw_user")
    currency = models.CharField(choices=withdrawType, max_length=10)
    address = models.CharField(default="", max_length=50)
    status = models.BooleanField(default=False)
    dollarAmount = models.FloatField(default=0)
    cryptoPayment = models.FloatField(default=0)
    createdOn = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=300,default="")
    check = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class SupportTicket(models.Model):
    user = models.ForeignKey("account.Account", on_delete=CASCADE, related_name="ticket_user")
    createdOn = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(default="", max_length=300)
    prob = models.TextField()


