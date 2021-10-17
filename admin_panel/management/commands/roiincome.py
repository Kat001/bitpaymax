from django.core.management.base import BaseCommand
from django.utils import timezone
from profile_app.models import Roiincome,Package,LevelIncome
from account.models import Account 

class Command(BaseCommand):
    help = 'Roi Income'
    
    def sendLevelIncome(self,userId,income):

        try:
            user = Account.objects.get(id=userId)

            # send 1 level Income...
            firstleveluser = user.sponsor
            if firstleveluser.is_active1 and firstleveluser.is_able_for_income:
                levelincome = LevelIncome(user=firstleveluser, from_user=user, 
                level="1", income=(income*15)/100)
                levelincome.save()
                firstleveluser.total_level_income += (income*15)/100
                firstleveluser.total_income += (income*15)/100
                firstleveluser.available_amount += (income*15)/100
                firstleveluser.save()

            # send 2 level Income...
            secondleveluser = firstleveluser.sponsor
            if secondleveluser.is_active1 and secondleveluser.is_able_for_income:
                levelincome = LevelIncome(user=secondleveluser, from_user=user, 
                level="2", income=(income*12)/100)
                levelincome.save()
                secondleveluser.total_level_income += (income*12)/100
                secondleveluser.total_income += (income*12)/100
                secondleveluser.available_amount += (income*12)/100
                secondleveluser.save()

            # send 3 level Income...
            thirdleveluser = secondleveluser.sponsor
            if thirdleveluser.is_active1 and thirdleveluser.is_able_for_income:
                levelincome = LevelIncome(user=thirdleveluser, from_user=user, 
                level="3", income=(income*9)/100)
                levelincome.save()
                thirdleveluser.total_level_income += (income*9)/100
                thirdleveluser.total_income += (income*9)/100
                thirdleveluser.available_amount += (income*9)/100
                thirdleveluser.save()


            # send 4 level Income...
            fourthleveluser = thirdleveluser.sponsor
            if fourthleveluser.is_active1 and fourthleveluser.is_able_for_income:
                levelincome = LevelIncome(user=fourthleveluser, from_user=user, 
                level="4", income=(income*9)/100)
                levelincome.save()
                fourthleveluser.total_level_income += (income*9)/100
                fourthleveluser.total_income += (income*9)/100
                fourthleveluser.available_amount += (income*9)/100
                fourthleveluser.save()

            # send 5 level Income...
            fifthleveluser = fourthleveluser.sponsor
            if fifthleveluser.is_active1 and fifthleveluser.is_able_for_income:
                levelincome = LevelIncome(user=fifthleveluser, from_user=user, 
                level="5", income=(income*9)/100)
                levelincome.save()
                fifthleveluser.total_level_income += (income*9)/100
                fifthleveluser.total_income += (income*9)/100
                fifthleveluser.available_amount += (income*9)/100
                fifthleveluser.save()


            # send 6 level Income...
            sixthleveluser = fifthleveluser.sponsor
            if sixthleveluser.is_active1 and sixthleveluser.is_able_for_income:
                levelincome = LevelIncome(user=sixthleveluser, from_user=user, 
                level="6", income=(income*6)/100)
                levelincome.save()
                sixthleveluser.total_level_income += (income*6)/100
                sixthleveluser.total_income += (income*6)/100
                sixthleveluser.available_amount += (income*6)/100
                sixthleveluser.save()

            # send 7 level Income...
            sevenleveluser = sixthleveluser.sponsor
            if sevenleveluser.is_active1 and sevenleveluser.is_able_for_income:
                levelincome = LevelIncome(user=sevenleveluser, from_user=user, 
                level="7", income=(income*6)/100)
                levelincome.save()
                sevenleveluser.total_level_income += (income*6)/100
                sevenleveluser.total_income += (income*6)/100
                sevenleveluser.available_amount += (income*6)/100
                sevenleveluser.save()

            # send 8 level Income...
            eightleveluser = sevenleveluser.sponsor
            if eightleveluser.is_active1 and eightleveluser.is_able_for_income:
                levelincome = LevelIncome(user=eightleveluser, from_user=user, 
                level="8", income=(income*6)/100)
                levelincome.save()
                eightleveluser.total_level_income += (income*6)/100
                eightleveluser.total_income += (income*6)/100
                eightleveluser.available_amount += (income*6)/100
                eightleveluser.save()


            # send 9 level Income...
            nineleveluser = eightleveluser.sponsor
            if nineleveluser.is_active1 and nineleveluser.is_able_for_income:
                levelincome = LevelIncome(user=nineleveluser, from_user=user, 
                level="9", income=(income*6)/100)
                levelincome.save()
                nineleveluser.total_level_income += (income*6)/100
                nineleveluser.total_income += (income*6)/100
                nineleveluser.available_amount += (income*6)/100
                nineleveluser.save()

            # send 10 level Income...
            tenleveluser = nineleveluser.sponsor
            if tenleveluser.is_active1 and tenleveluser.is_able_for_income:
                levelincome = LevelIncome(user=tenleveluser, from_user=user, 
                level="10", income=(income*6)/100)
                levelincome.save()
                tenleveluser.total_level_income += (income*6)/100
                tenleveluser.total_income += (income*6)/100
                tenleveluser.available_amount += (income*6)/100
                tenleveluser.save()

            # send 11 level Income...
            elevenleveluser = tenleveluser.sponsor
            if elevenleveluser.is_active1 and elevenleveluser.is_able_for_income:
                levelincome = LevelIncome(user=elevenleveluser, from_user=user, 
                level="11", income=(income*4)/100)
                levelincome.save()
                elevenleveluser.total_level_income += (income*4)/100
                elevenleveluser.total_income += (income*4)/100
                elevenleveluser.available_amount += (income*4)/100
                elevenleveluser.save()

            # send 12 level Income...
            twelveleveluser = elevenleveluser.sponsor
            if twelveleveluser.is_active1 and twelveleveluser.is_able_for_income:
                levelincome = LevelIncome(user=twelveleveluser, from_user=user, 
                level="12", income=(income*4)/100)
                levelincome.save()
                twelveleveluser.total_level_income += (income*4)/100
                twelveleveluser.total_income += (income*4)/100
                twelveleveluser.available_amount += (income*4)/100
                twelveleveluser.save()

            # send 13 level Income...
            thirteenleveluser = twelveleveluser.sponsor
            if thirteenleveluser.is_active1 and thirteenleveluser.is_able_for_income:
                levelincome = LevelIncome(user=thirteenleveluser, from_user=user, 
                level="13", income=(income*4)/100)
                levelincome.save()
                thirteenleveluser.total_level_income += (income*4)/100
                thirteenleveluser.total_income += (income*4)/100
                thirteenleveluser.available_amount += (income*4)/100
                thirteenleveluser.save()

            # send 14 level Income...
            fourtheenleveluser = thirteenleveluser.sponsor
            if fourtheenleveluser.is_active1 and fourtheenleveluser.is_able_for_income:
                levelincome = LevelIncome(user=fourtheenleveluser, from_user=user, 
                level="14", income=(income*4)/100)
                levelincome.save()  
                fourtheenleveluser.total_level_income += (income*4)/100
                fourtheenleveluser.total_income += (income*4)/100
                fourtheenleveluser.available_amount += (income*4)/100
                fourtheenleveluser.save() 

            # send 15 level Income...
            fiftheenleveluser = fourtheenleveluser.sponsor
            if fiftheenleveluser.is_active1 and fiftheenleveluser.is_able_for_income:
                levelincome = LevelIncome(user=fiftheenleveluser, from_user=user, 
                level="15", income=(income*4)/100)
                levelincome.save()
                fiftheenleveluser.total_level_income += (income*4)/100
                fiftheenleveluser.total_income += (income*4)/100
                fiftheenleveluser.available_amount += (income*4)/100
                fiftheenleveluser.save() 

# --------------------------------------------------------------------#
#                      |  # Super Level Income |                      #
# --------------------------------------------------------------------#

            # send 16 level Income...
            sixteenleveluser = fiftheenleveluser.sponsor
            pack50  = Package.objects.get(amount=50)
            if sixteenleveluser.is_active1 and sixteenleveluser.is_able_for_income and pack50 in  sixteenleveluser.supper_packages.all():
                levelincome = LevelIncome(user=sixteenleveluser, from_user=user, 
                level="16", income=(income*3)/100)
                levelincome.save()
                sixteenleveluser.total_level_income += (income*3)/100
                sixteenleveluser.total_income += (income*3)/100
                sixteenleveluser.available_amount += (income*3)/100
                sixteenleveluser.save()

            # send 17 level Income...
            seventeenleveluser = sixteenleveluser.sponsor
            if seventeenleveluser.is_active1 and seventeenleveluser.is_able_for_income and pack50 in  seventeenleveluser.supper_packages.all():
                levelincome = LevelIncome(user=sixteenleveluser, from_user=user, 
                level="17", income=(income*3)/100)
                levelincome.save()
                seventeenleveluser.total_level_income += (income*3)/100
                seventeenleveluser.total_income += (income*3)/100
                seventeenleveluser.available_amount += (income*3)/100
                seventeenleveluser.save()   

            # send 18 level Income...
            eightteenleveluser = seventeenleveluser.sponsor
            if eightteenleveluser.is_active1 and eightteenleveluser.is_able_for_income and pack50 in  eightteenleveluser.supper_packages.all():
                levelincome = LevelIncome(user=eightteenleveluser, from_user=user, 
                level="18", income=(income*3)/100)
                levelincome.save()
                eightteenleveluser.total_level_income += (income*3)/100
                eightteenleveluser.total_income += (income*3)/100
                eightteenleveluser.available_amount += (income*3)/100
                eightteenleveluser.save() 

            # send 19 level Income...
            nineteenleveluser = eightteenleveluser.sponsor
            pack100  = Package.objects.get(amount=100)
            if nineteenleveluser.is_active1 and nineteenleveluser.is_able_for_income and pack100 in  nineteenleveluser.supper_packages.all():
                levelincome = LevelIncome(user=nineteenleveluser, from_user=user, 
                level="19", income=(income*2)/100)
                levelincome.save()
                nineteenleveluser.total_level_income += (income*2)/100
                nineteenleveluser.total_income += (income*2)/100
                nineteenleveluser.available_amount += (income*2)/100
                nineteenleveluser.save() 

            # send 20 level Income...
            twenteelevel = nineteenleveluser.sponsor
            if twenteelevel.is_active1 and twenteelevel.is_able_for_income and pack100 in  twenteelevel.supper_packages.all():
                levelincome = LevelIncome(user=twenteelevel, from_user=user, 
                level="20", income=(income*2)/100)
                levelincome.save()
                twenteelevel.total_level_income += (income*2)/100
                twenteelevel.total_income += (income*2)/100
                twenteelevel.available_amount += (income*2)/100
                twenteelevel.save()     

            # send 21 level Income...
            twenteeonelevel = twenteelevel.sponsor
            pack250  = Package.objects.get(amount=250)
            if twenteeonelevel.is_active1 and twenteeonelevel.is_able_for_income and pack250 in  twenteeonelevel.supper_packages.all():
                levelincome = LevelIncome(user=twenteeonelevel, from_user=user, 
                level="21", income=(income*1)/100)
                levelincome.save()
                twenteeonelevel.total_level_income += (income*1)/100
                twenteeonelevel.total_income += (income*1)/100
                twenteeonelevel.available_amount += (income*1)/100
                twenteeonelevel.save()    

            # send 22 level Income...
            twenteetwolevel = twenteeonelevel.sponsor
            if twenteetwolevel.is_active1 and twenteetwolevel.is_able_for_income and pack250 in  twenteetwolevel.supper_packages.all():
                levelincome = LevelIncome(user=twenteetwolevel, from_user=user, 
                level="22", income=(income*1)/100)
                levelincome.save()
                twenteetwolevel.total_level_income += (income*1)/100
                twenteetwolevel.total_income += (income*1)/100
                twenteetwolevel.available_amount += (income*1)/100
                twenteetwolevel.save() 

            # send 23 level Income...
            twenteethreelevel = twenteetwolevel.sponsor
            pack500  = Package.objects.get(amount=500)
            if twenteethreelevel.is_active1 and twenteethreelevel.is_able_for_income and pack250 in  twenteethreelevel.supper_packages.all():
                levelincome = LevelIncome(user=twenteethreelevel, from_user=user, 
                level="23", income=(income*1)/100)
                levelincome.save()
                twenteethreelevel.total_level_income += (income*1)/100
                twenteethreelevel.total_income += (income*1)/100
                twenteethreelevel.available_amount += (income*1)/100
                twenteethreelevel.save()   

            # send 24 level Income...
            twenteefourlevel = twenteethreelevel.sponsor
            if twenteefourlevel.is_active1 and twenteefourlevel.is_able_for_income and pack250 in  twenteefourlevel.supper_packages.all():
                levelincome = LevelIncome(user=twenteefourlevel, from_user=user, 
                level="24", income=(income*1)/100)
                levelincome.save()
                twenteefourlevel.total_level_income += (income*1)/100
                twenteefourlevel.total_income += (income*1)/100
                twenteefourlevel.available_amount += (income*1)/100
                twenteefourlevel.save()   

            # send 25 level Income...
            twenteefivelevel = twenteefourlevel.sponsor
            if twenteefivelevel.is_active1 and twenteefivelevel.is_able_for_income and pack250 in  twenteefivelevel.supper_packages.all():
                levelincome = LevelIncome(user=twenteefivelevel, from_user=user, 
                level="24", income=(income*1)/100)
                levelincome.save()
                twenteefivelevel.total_level_income += (income*1)/100
                twenteefivelevel.total_income += (income*1)/100
                twenteefivelevel.available_amount += (income*1)/100
                twenteefivelevel.save()       


        except Exception as e:
            print(e)


    def handle(self, *args, **kwargs):
        try:
            allActiveUsers = Account.objects.filter(is_active1=True)
            for user in allActiveUsers:
                if user.is_able_for_income:
                    for package in user.packages.all():
                        if Roiincome.objects.filter(user=user, package=package).count() <= 300:
                            income = (package.amount*1)/100
                            roi_obj = Roiincome(user=user, package=package, income=income)
                            roi_obj.save()

                            #update roiincome....
                            user.total_roi_income += income

                            #update available income.....
                            user.available_amount += income

                            # update total income.....
                            user.total_income += income

                            user.save()

                            self.sendLevelIncome(user.id,income)

        except Exception as e:
            print(e)
