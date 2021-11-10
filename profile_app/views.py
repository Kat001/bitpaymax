from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import update_session_auth_hash
from account.models import Account
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from profile_app.models import Fund
from profile_app.models import Package
from profile_app.models import Fundrecord
from profile_app.models import LevelIncome
from profile_app.models import Roiincome
from profile_app.models import Withdrawal
from profile_app.models import SupportTicket
from payment.models import Bank_Info

from django.db.models import Sum



# Create your views here

@login_required
def profile(request):
    user = request.user
    fund_obj = Fund.objects.get(user = user)
    
    try:
        remain_price = (3 * user.packages.all().aggregate(Sum('amount')).get('amount__sum')) - user.total_income
    except Exception as e:
        remain_price = 0

    d = {
        'remain_price' : remain_price,
        'fund_obj' : fund_obj
    }
    return render(request,'profile1.html',d)

@login_required
def personalInfo(request):
    return render(request,'personalinfo.html')

@login_required
def updateProfile(request):
    user = request.user
    name = user.username
    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        mobile_no = request.POST.get('mobile')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')
        myfile = request.FILES['myfile']
        p = request.POST.get('txn_pass')

        
        if p == user.txn_password:
            user.first_name = f_name
            user.phon_no = mobile_no
            user.address = address
            user.state = state
            user.city = city
            user.zip = zip
            user.image = myfile
            user.save()
            messages.success(request,'Profile Updated successfully!!')
            return redirect('updateprofile')
        else:
            messages.error(request,'Wrong Transection password!!')
            return redirect('updateprofile')
    else:
        pass
    return render(request,'updateprofile.html')

@login_required
def changePassword(request):
    user = request.user
    user_pass = user.password

    if request.method == 'POST':
        o_pass = request.POST.get('o_pass')
        n_pass = request.POST.get('n_pass')
        c_pass = request.POST.get('c_pass')

        cheak = user.check_password(o_pass)

        if cheak:
            if n_pass == c_pass:
                p = make_password(n_pass)
                user.set_password(n_pass)
                user.save()
                update_session_auth_hash(request,user)
                messages.success(request,"Password Changed successfully!!")
                return redirect('changepassword')
            else:
                messages.error(request,'New password and confirm password should be same!!')
                return redirect('changepassword')
        else:
            messages.error(request,"Old Password is Wrong!!")
            return redirect('changepassword')
    return render(request,'changepassword.html')

@login_required
def changeTxnPassword(request):
    user = request.user
    user_t_pass = user.txn_password

    if request.method == 'POST':
        o_pass = request.POST.get('o_pass')
        n_pass = request.POST.get('n_pass')
        c_pass = request.POST.get('c_pass')

        if user_t_pass == o_pass:
            if n_pass == c_pass:
                user.txn_password = n_pass
                user.save()
                messages.success(request,'Txn password changed successfully!!')
            else:
                messages.error(request,'New password and confirm password should be same!!')
                return redirect('changetxnpassword')
        else:
            messages.error(request,'Old Txn Password is Wrong!!')
            return redirect('changetxnpassword')

    return render(request,'changetxnpassword.html')

@login_required
def addFund(request):
    return render(request,'addfund.html')

@login_required
def activateId(request):
    user = request.user
    fund_obj = Fund.objects.get(user=user)
    d = {
        'fund' : fund_obj,
    }
    return render(request,'activateid.html',d)

@login_required
def activateIdAmount(request,amount):
    user = request.user
    amount = int(amount.replace(" $",""))
    try:
        package = Package.objects.get(amount=amount)
        fund = Fund.objects.get(user=user)
        if fund.available_fund >= amount:
            if package in user.packages.all():
                messages.error(request,'This Package is Already Purchased!')
                return redirect('activateid')
            else:
                fund.available_fund -= amount
                user.packages.add(package)
                user.is_active1 = True
                user.is_able_for_income = True
                fund.save()
                user.save()
                messages.success(request,"Package Purchased Successfully!")
                return redirect('activateidamount')

        else:
            messages.error(request,'Not Enough Balance For This Package!')
            return redirect('activateid')
        user.packages.add(package)
        user.save()
    except Exception as e:
        print(e)
        pass
    return render(request,'activateidamount.html')

@login_required
def activateTeamId(request):
    user = request.user
    fund_obj = Fund.objects.get(user=user)
    if request.method == "POST":
        print("post called")
    d = {
        'fund' : fund_obj,
    }
    return render(request,'activateteamidamount.html',d)

@login_required
def activateTeamIDAmount(request,amount,userid):
    user = request.user
    amount = int(amount.replace(" $",""))
    try:
        package = Package.objects.get(amount=amount)
        fund = Fund.objects.get(user=user)
        if fund.available_fund >= amount:
            if package in user.packages.all():
                messages.error(request,'This Package is Already Purchased!')
                return redirect('activateteamid')
            else:
                activatedUser = Account.objects.get(username=userid)
                fund.available_fund -= amount
                activatedUser.packages.add(package)
                activatedUser.is_active1 = True
                activatedUser.is_able_for_income = True
                fund.save()
                user.save()
                activatedUser.save()
                messages.success(request,"Package Purchased Successfully!")
                return redirect('activateteamid')
        else:
            messages.error(request,'Not Enough Balance For This Package!')
            return redirect('activateteamid')

    except Account.DoesNotExist:
        print("accoynt does not exxll")
        messages.error(request,'User id is wrong!')
        return redirect('activateteamid')
    except Exception as e:
        messages.error(request,str(e))
        return redirect('activateteamid')
    return render(request,'activateteamidamount.html')


@login_required
def transferFund(request):
    user = request.user
    obj = Fund.objects.get(user=user)
    

    if request.method == 'POST':
        username       = request.POST.get('user_name')
        amount          = request.POST.get('amount')
        txn_pass        = request.POST.get('txn_pass')

        try:
            if user.txn_password == txn_pass:
                if username != user.username:
                    user1 = Account.objects.get(username=username)
                    u_id_obj = Fund.objects.get(user=user1)

                    if obj.available_fund >= int(amount):
                        u_id_obj.available_fund += int(amount)
                        obj.available_fund -= int(amount)
                        u_id_obj.save()
                        obj.save()

                        obj_hist = Fundrecord(user=user,to_user=user1,amount=int(amount),fundType="TFS")
                        obj_hist.save()

                        messages.success(request,'Fund Transfered successfully!!')
                        return redirect('transferfund')

                    else:
                        messages.error(request,'Not Enough Amount!!')
                        return redirect('transferfund')
                else:
                    messages.error(request,'U entered your own id!!')
                    return redirect('transferfund')
            else:
                messages.error(request,'Wrong Txn Password!!')
                return redirect('transferfund')
        except Exception as e:
            print(e)
            messages.error(request,'User id does not exist!!')
            return redirect('transferfund')

    d = {
        'obj' : obj,
    }
    return render(request,'transferfund.html',d)

@login_required
def transferFundHistory(request):
    user = request.user
    userTransfer_obj = Fundrecord.objects.filter(user=user)
    fund = Fund.objects.get(user=user)
    page = request.GET.get('page', 1)
    paginator = Paginator(userTransfer_obj, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    d = {
        'users':users,
        'fund' : fund,  
    } 
    return render(request,'transferfundhistory.html',d)


@login_required
def referralTeam(request,user_id):

    #make 100 users
    # spn = Account.objects.get(username="admin")
    # for i in range(101):
    #     obj = Account(username="BPM"+str(i),password='1000',txn_password="jj",sponsor=spn)
    #     obj.save()


    user = Account.objects.get(id=user_id)
    directUsers = Account.objects.filter(sponsor = user).order_by('-date_joined')
    print(directUsers)
    page = request.GET.get('page', 1)
    paginator = Paginator(directUsers, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    d = {
        'users':users,
        }

    return render(request,'referralteam.html',d)

def myPacks(request):
    user = request.user
    packs = user.packages.all()
    fund_obj = Fund.objects.get(user=user)

    if request.method=="POST":
        amount = float(request.POST.get('amount'))
        Flag = False
        try:
            pack = Package.objects.get(amount=amount)
            
            if pack in user.supper_packages.all():
                messages.error(request,'This Supper Pack Already Purchased!')
                return redirect('mypacks')
            
            if amount <= fund_obj.available_fund:
                if amount == 50:
                    user.supper_packages.add(pack)
                    user.save()
                    fund_obj.available_fund -= amount
                    fund_obj.save()
                    messages.success(request,"Purchased Successfully!!")
                    return redirect('mypacks')
                
                elif amount == 100:
                    pack50 = Package.objects.get(amount=50)
                    if pack50 in user.supper_packages.all():
                        user.supper_packages.add(pack)
                        user.save()
                        fund_obj.available_fund -= amount
                        fund_obj.save()
                        messages.success(request,"Purchased Successfully!!")
                        return redirect('mypacks')
                    else:
                        messages.error(request,"Not Able For This Pack, First purchase 50 $")
                        return redirect('mypacks')
                
                elif amount == 250:
                    pack100 = Package.objects.get(amount=100)
                    if pack100 in user.supper_packages.all():
                        user.supper_packages.add(pack)
                        fund_obj.available_fund -= amount
                        fund_obj.save()
                        user.save()
                        messages.success(request,"Purchased Successfully!!")
                        return redirect('mypacks')
                    else:
                        messages.error(request,"Not Able For This Pack, First purchase 100 $")
                        return redirect('mypacks')
                
                elif amount == 500:
                    pack250 = Package.objects.get(amount=250)
                    if pack250 in user.supper_packages.all():
                        user.supper_packages.add(pack)
                        user.save()
                        fund_obj.available_fund -= amount
                        fund_obj.save()
                        messages.success(request,"Purchased Successfully!!")
                        return redirect('mypacks')
                    else:
                        messages.error(request,"Not Able For This Pack, First purchase 250 $")
                        return redirect('mypacks')
                
                else:
                    messages.error(request,'Not Effetctive pack!')
                    return redirect('mypacks')

            else:
                messages.error(request,'Not Enough Fund For Activation!')
                return redirect('mypacks')
                
        except Exception as e:
            print(e)
            messages.error(request,str(e))
            return redirect('mypacks')

    d ={
        'packs' : packs,
    }
    return render(request,'mypacks.html',d)

@login_required
def levelTeam(request):
    user = request.user
    directUsers = Account.objects.filter(sponsor = user).order_by('-date_joined')
    page = request.GET.get('page', 1)
    paginator = Paginator(directUsers, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    d = {
        'users':users,
        }
    return render(request,'levelteam/levelteam.html',d)

@login_required
def levelTeam2(request):
    user = request.user
    l = []

    objs1 = Account.objects.filter(sponsor=user)

    for o in objs1:
        obj2 = Account.objects.filter(sponsor=o)
        for i in obj2:
            l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    page = request.GET.get('page', 1)
    paginator = Paginator(objs, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    # myfilter = Account_Filter(request.GET,queryset=objs)
    # objs  = myfilter.qs

    d = {
        'users' : users,
    }
    return render(request,'levelteam/levelteam2.html',d)

@login_required
def levelTeam3(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponsor=user)

    for o in objs1:
        obj2 = Account.objects.filter(sponsor=o)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponsor=o2)
            for i in obj3:
                l.append(i.id)
    objs = Account.objects.filter(id__in=l)
    page = request.GET.get('page', 1)
    paginator = Paginator(objs, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    # myfilter = Account_Filter(request.GET,queryset=objs)
    # objs  = myfilter.qs

    d = {
        'users':users,  
    }
    return render(request,'levelteam/levelteam3.html',d)

@login_required
def levelTeam4(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponsor=user)

    for o in objs1:
        obj2 = Account.objects.filter(sponsor=o)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponsor=o2)
            for o3 in obj3:
                obj4 = Account.objects.filter(sponsor=o3)
                for i in obj4:
                    l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    page = request.GET.get('page', 1)
    paginator = Paginator(objs, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    # myfilter = Account_Filter(request.GET,queryset=objs)
    # objs  = myfilter.qs

    d = {
        'users':users,
    }
    return render(request,'levelteam/levelteam4.html',d)

@login_required
def levelTeam5(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponsor=user)

    for o in objs1:
        obj2 = Account.objects.filter(sponsor=o)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponsor=o2)
            for o3 in obj3:
                obj4 = Account.objects.filter(sponsor=o3)
                for i in obj4:
                    l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    page = request.GET.get('page', 1)
    paginator = Paginator(objs, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)



    

    # myfilter = Account_Filter(request.GET,queryset=objs)
    # objs  = myfilter.qs

    d = {
        'users':users,
    }
    return render(request,'profile_templates/levelteam4.html',d)

def levelTeam5(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponsor=user)

    for o in objs1:
        obj2 = Account.objects.filter(sponsor=o)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponsor=o2)
            for o3 in obj3:
                obj4 = Account.objects.filter(sponsor=o3)
                for o4 in obj4:
                    obj5 = Account.objects.filter(sponsor=o4)
                    for i in obj5:
                        l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    page = request.GET.get('page', 1)
    paginator = Paginator(objs, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)



    # myfilter = Account_Filter(request.GET,queryset=objs)
    # objs  = myfilter.qs

    d = {
        'users':users,

    }
    return render(request,'levelteam/levelteam5.html',d)

@login_required
def withdrawal(request):
    user = request.user
    fund_obj = Fund.objects.get(user = user)

    if request.method == 'POST':
        currency = request.POST.get('currency')
        dollarAmount = float(request.POST.get('dollorAmount'))
        if currency == "1":
            selectedCurrency = "INR"
        elif currency == "2":
            selectedCurrency = "TRX"
        elif currency == "3":
            selectedCurrency = "ETH"
        elif currency == "4":
            selectedCurrency = "BTC"

        try:
            if dollarAmount >= 10 and dollarAmount <= float(user.available_amount):
                user.available_amount -= dollarAmount
                withdrawal = Withdrawal(user=user, currency=selectedCurrency, dollarAmount=dollarAmount)
                withdrawal.save()
                user.save()
                messages.success(request,'Request Submitted Successfully!')
                return redirect('withdrawal')

            else:
                messages.error(request,'Not Enough balance to Withdraw!!')
                return redirect('withdrawal')

        except Exception as e:
            print(e)

    d = {
        'fund_obj' : fund_obj,
    }
    return render(request,'withdrawal.html',d)

@login_required
def withdrawalHistory(request):
    user = request.user
    directUsers = Withdrawal.objects.filter(user = user).order_by('-createdOn')
    print(directUsers)
    page = request.GET.get('page', 1)
    paginator = Paginator(directUsers, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    d = {
        'users':users,
        }
    return render(request,'withdrawalhistory.html',d)

@login_required
def supportTicket(request):
    user = request.user
    tickets = SupportTicket.objects.filter(user=user)

    if request.method == 'POST':
        try:
            subject = request.POST.get('subject')
            department = request.POST.get('department')
            msg = request.POST.get('message')
            obj = SupportTicket(user=user,subject=subject,prob=msg)
            obj.save()
            return redirect('supportticket')
        except Exception as e:
            pass


    d = {
        'tickets' : tickets,
    }
    return render(request,'supportticket.html',d)

@login_required
def supportTicketHistory(request):
    return render(request,'supporttickethistory.html')


def levelIncome(request):
    user = request.user
    directUsers = LevelIncome.objects.filter(user = user).order_by('-date')
    print(directUsers)
    page = request.GET.get('page', 1)
    paginator = Paginator(directUsers, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    d = {
        'users':users,
        }


    return render(request,'levelincome.html',d)

def roiIncome(request):
    user = request.user
    directUsers = Roiincome.objects.filter(user = user).order_by('-createdOn')
    print(directUsers)
    page = request.GET.get('page', 1)
    paginator = Paginator(directUsers, 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    d = {
        'users':users,
        }

    return render(request,'roiincome.html',d)

def adminWithdrawal(request):
    user = request.user
    if user.is_superuser:
        directUsers = Withdrawal.objects.filter(check=False).order_by('createdOn')
        print(directUsers)
        page = request.GET.get('page', 1)
        paginator = Paginator(directUsers, 10)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        users = []

    d = {
        'users':users,
        }

    return render(request,'adminwithdrawal.html',d)

def adminWithdrawalCancel(request,iid):
    user = request.user
    if user.is_superuser:
        # Do all the canceletion part here
        w_obj = Withdrawal.objects.get(id=iid)
        w_obj.check = True
        w_obj.user.available_amount += w_obj.dollarAmount
        w_obj.user.save()
        w_obj.save()
        
        
        directUsers = Withdrawal.objects.filter(check=False).order_by('createdOn')
        print(directUsers)
        page = request.GET.get('page', 1)
        paginator = Paginator(directUsers, 10)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        users = []

    d = {
        'users':users,
        }
    return render(request,'adminwithdrawal.html',d)


def adminWithdrawalAccept(request,iid):
    user = request.user
    if user.is_superuser:
        directUsers = Withdrawal.objects.filter(check=False).order_by('createdOn')
        print(directUsers)
        page = request.GET.get('page', 1)
        paginator = Paginator(directUsers, 10)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    else:
        users = []

    d = {
        'users':users,
        }
    return render(request,'adminwithdrawal.html',d)

@login_required
def bankDetails(request):
    user = request.user
    d = {}
    try:
        bank_detail = Bank_Info.objects.get(user=user)
        bank = True
        d['bank'] = bank
        d['bank_detail'] = bank_detail
    except Bank_Info.DoesNotExist:
        bank = False

    if request.method == 'POST':
        account_holder_name = request.POST.get('accountholdername')
        bank_name = request.POST.get('bankname')
        account_no = request.POST.get('accountno')
        confirm_account_no = request.POST.get('confirmaccountno')
        ifsc_ecode = request.POST.get('ifscecode')
        branch_name = request.POST.get('branchname')
        transaction_pass = request.POST.get('txn_pass')
        
        if transaction_pass == user.txn_password:
            if account_no == confirm_account_no:
                bank_obj = Bank_Info(user=user,account_holder_name=account_holder_name, 
                            account_number=account_no, branch_name=branch_name, ifsc_code=ifsc_ecode,
                            bank_name=bank_name, )
                bank_obj.save()
                return redirect('bankdetails')
            else:
                messages.error(request,'Account no and confirm account no are not same!!')
                return redirect('bankdetails')
        else:
            messages.error(request,'Wrong Transaction Password!!')
            return redirect('bankdetails')            

    return render(request,'bankdetails.html',d)