from django.shortcuts import render,redirect
from coinpayments import CoinPaymentsAPI
from django.conf import settings
from django.contrib.auth.decorators import login_required
from profile_app.models import Fund
from payment.models import ExchangeRates
from payment.models import Payment
from profile_app.models import Fund
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Account



import razorpay
import requests
import pdb
import random


# Create your views here.

@login_required
def createTransaction(request):
    user = request.user
    fund = Fund.objects.get(user=user)
    rate = ExchangeRates.objects.last()
    if request.method == 'POST':
        try:
            currency = request.POST.get('currency')
            dollarAmount = float(request.POST.get('dollorAmount'))
        except Exception as e:
            currency = 1
            dollarAmount = 0

            
        if currency == "1":
            selectedCurrency = "INR"
        elif currency == "2":
            selectedCurrency = "TRX"
        elif currency == "3":
            selectedCurrency = "ETH"
        elif currency == "4":
            selectedCurrency = "BTC"

        try:
            if selectedCurrency in ["TRX", "ETH", "BTC"]:
                api = CoinPaymentsAPI(public_key=settings.COINPAYMENTS_API_KEY, 
                    private_key=settings.COINPAYMENTS_API_SECRET)
                res = api.create_transaction(amount=dollarAmount, 
                    currency1="USD", currency2=selectedCurrency, buyer_email="dev@gmail.com", 
                    )

                if res['error'] == "ok":
                    payment = Payment(user=user, currency=selectedCurrency, address=res["result"]["address"], 
                    txId=res["result"]["txn_id"], dollarAmount=dollarAmount, cryptoPayment=res["result"]["amount"])
                    payment.save()

                request.session['payment_id'] = payment.id
                request.session['tx_id'] = res["result"]["txn_id"]
                request.session['address'] = res["result"]["address"]
                request.session['qr_code'] = res["result"]["qrcode_url"]
                request.session['currency'] = selectedCurrency
                request.session['amount'] = res["result"]["amount"]
                request.session['dollarAmount'] = dollarAmount
                return redirect('checktransaction')
            
            elif selectedCurrency == 'INR':  
                
                payment_obj = Payment(user=user, currency=selectedCurrency, 
                    txId="paymentClient['id']", dollarAmount=dollarAmount,)
                payment_obj.save()
                request.session['payment_id'] = payment_obj.id
                request.session['dollarAmount'] = dollarAmount

                while True:
                    mtx = str(random.randint(1,2000000))
                    if mtx not in Payment.objects.values_list('mtx',flat=True):
                        break
                    else:
                        pass
                payload = {
                    "amount": dollarAmount*75,
                    "udf": user.username,
                    "contact_number": user.phon_no,
                    "email_id": user.email,
                    "currency": "INR",
                    "mtx": mtx+"-"+user.username
                }
                
                headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": settings.OPENBANK_AUTH
                }
                
                url = settings.OPENBANK_BASE_URL+'/api/payment_token'
                response = requests.request("POST", url, json=payload, headers=headers)
                res_data = response.json()
                print(res_data)
                print("id is:",res_data['id'])
                if res_data['id']:
                    payment_obj.mtx = res_data['mtx']
                    payment_obj.save()
                    return render(request,'createtransaction.html',{
                        'payment':True,
                        'fund' : fund,
                        'token_id':res_data['id'],
                        'remote_script' : "https://payments.open.money/layer",
                        "accesskey": settings.OPENBANK_API_KEY,
                        })        
                else:
                    return render(request,'createtransaction.html',{'fund' : fund})        
        
        except Exception as e:
            print(e)
            pass
    
    else:
        pass

    d = {
        'fund' : fund,
        'rate' : rate,
    }
    return render(request,'createtransaction.html', d)

def checkTransaction(request):
    tx_id = request.session['tx_id']
    address = request.session['address']
    qr_code = request.session['qr_code']
    currency = request.session['currency']
    amount = request.session['amount']
    
    api = CoinPaymentsAPI(public_key=settings.COINPAYMENTS_API_KEY, 
            private_key=settings.COINPAYMENTS_API_SECRET)
    res = api.get_tx_info(txid=tx_id)
    
    if res['result']['status'] == 1:
        return redirect('paymentsuccess')

    d = {
        'data': "k",
        'address': address,
        'qr_code': qr_code,
        'currency': currency,
        'amount': amount
    }
    return render(request,"payment.html",d)

def paymentSuccess(request):
    user_obj = request.user
    amount = request.session['dollarAmount']
    paymentId = int(request.session['payment_id'])
    payment = Payment.objects.get(id=paymentId)
    
    try:
        fund_obj = Fund.objects.get(user = user_obj)
        fund_obj.available_fund += float(amount)
        fund_obj.save()
        payment.status = True
        payment.save()
    except Exception as e:
        pass
    return render(request,'paymentsuccess.html')

def payout(request):
    print("payout rill statreted")
    payload = {
        "bene_account_number": "string",
        "ifsc_code": "string",
        "recepient_name": "string",
        "email_id": "string",
        "mobile_number": "string",
        "otp": "string",
        "debit_account_number": "string",
        "transaction_types_id": 0,
        "amount": "string",
        "merchant_ref_id": "string",
        "purpose": "string",
        "vpa": "string"
    }
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": settings.OPENBANK_AUTH
    }
    
    url = settings.OPENBANK_BASE_URL +'/1/payouts/otp'
    response = requests.request("POST", url, headers=headers)
    print(response.text)
    return render(request,'createtransaction.html')



class PaymentCallback(APIView):
  
    def post(self, request, format=None):
        print(request)
        print(request.data)
        try:
            if request.data['event'] == "payment_token_paid" and request.data['status']=="paid":
                user_name = request.data['mtx'].split('-')[1]
                payment_obj = Payment.objects.get(mtx=request.data['mtx'])
                payment_obj.status = True
                payment_obj.save()
                user_obj = Account.objects.get(username=user_name)
                fund_obj = Fund.objects.get(user = user_obj)
                fund_obj.available_fund += float(request.data['amount'])/75
                fund_obj.save()
                user_obj.save()
                return Response("msgDone")
        except Exception as e:
            print(e)
            return Response("Not Done")
        return Response("msgDone")
