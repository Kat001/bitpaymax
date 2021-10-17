from django.core.management.base import BaseCommand
from django.utils import timezone
from profile_app.models import Roiincome,Package
from account.models import Account 
from django.db.models import Sum

class Command(BaseCommand):
    help = 'Update Able to income'
    def handle(self, *args, **kwargs):
        try:
            allActiveUsers = Account.objects.filter(is_active1=True)
            for user in allActiveUsers:
                alowable_income = 3 * user.packages.all().aggregate(Sum('amount')).get('amount__sum')
                if user.total_income >= alowable_income:
                    user.is_able_for_income = False
                    user.is_active1 = False
                    
                    # Remove all the packs fr
                    user.packages.clear()
                    user.total_income = 0
                    
                    user.save() 
                print(alowable_income)
        except Exception as e:
            print(e)
