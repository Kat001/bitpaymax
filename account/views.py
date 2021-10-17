from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
import random
from .models import Account
from django.contrib.auth import logout
from django.contrib.auth.models import auth
from profile_app.models import Fund



# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        sponsor = request.POST.get('sponsorid')
        mobile_no = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        txnPassword = request.POST.get('txnpass')
        fullName = request.POST.get('fullname')
        

        hax_password = make_password(password)

        if password != txnPassword:
            try:
                spn_obj = Account.objects.get(username=sponsor)
                while True:
                    rand_num = random.randint(500000,599999)
                    u_name = 'BPM' + str(rand_num)
                    if Account.objects.filter(username=u_name).exists():
                        pass
                    else:
                        break

                user = Account(username = u_name, sponsor=spn_obj,
                                password=hax_password,email=email,
                                txn_password=txnPassword,phon_no=mobile_no,
                                password1=password,first_name=fullName,
                                last_name="lName")

                user.save()
                fund = Fund(user = user)
                fund.save()

                # Send Id and pass on Mobile number with id and password.....
                messages.success(request,'User Created Successfully!!')
                return redirect('signin')


            except Exception as e:
                print(e)
                messages.error(request,"Sponsor Does Not Exist!!")
                return redirect('signup')
        else:
            messages.error(request,'Password and transection password can not be same!!')
            return redirect('signup')

    else:
        pass

    return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        pass1 = request.POST.get('password')


        user = auth.authenticate(username=u_name,password=pass1)

        if user is not None:
            auth.login(request,user)
            return redirect('profile')
        else:
            messages.error(request,'Wrong username or password!!')
            return redirect('signin')
    return render(request,'signin.html')
