from django.contrib import admin
from .models import ExchangeRates,Bank_Info,Payment
# Register your models here.

admin.site.register(ExchangeRates)
admin.site.register(Bank_Info)
admin.site.register(Payment)

