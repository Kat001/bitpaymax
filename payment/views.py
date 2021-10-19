from django.shortcuts import render,redirect
from coinpayments import CoinPaymentsAPI
from django.conf import settings
from django.contrib.auth.decorators import login_required
from profile_app.models import Fund
from payment.models import ExchangeRates
from payment.models import Payment
from profile_app.models import Fund

import razorpay
import requests
import pdb


# Create your views here.

@login_required
def createTransaction(request):
    user = request.user
    fund = Fund.objects.get(user=user)
    rate = ExchangeRates.objects.last()
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
                
                payload = {
                    "amount": dollarAmount*75,
                    "contact_number": user.phon_no,
                    "email_id": user.email,
                    "currency": "INR",
                    "mtx": str(payment_obj.id)
                }
                
                headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": settings.OPENBANK_AUTH
                }
                
                url = settings.OPENBANK_BASE_URL+'/api/payment_token'
                response = requests.request("POST", url, json=payload, headers=headers)
                res_data = response.json()
                print(response.text)
                print(res_data)
                if res_data['id']:
                    return render(request,'createtransaction.html',{
                        'payment':True,
                        'fund' : fund,
                        'token_id':res_data['id'],
                        'remote_script' : "https://sandbox-payments.open.money/layer",
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


def createOrder(request):

    payload = {
        "amount": 500,
        "udf": "string",
        "contact_number": "9012101244",
        "email_id": "dev@gmail.com",
        "currency": "INR",
        "mtx": "string111212"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": settings.OPENBANK_AUTH
        }

    response = requests.request("GET", url,headers=headers)
    print(response)

    print(response.text)

    d = {
        'token_id':"sb_pt_BTsdBdchq6jelvn",
        'remote_script' : "https://sandbox-payments.open.money/layer",
        "accesskey": 'c63d1670-300d-11ec-8522-7b6387f0dcea',
    }
    return render(request,'checkout.html',d)
