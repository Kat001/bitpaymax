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
                client = razorpay.Client(auth= ('rzp_test_L7FuyuMfhRJozZ','FvHFb8CHOsUQiYXeyrhbP5Ij'))
                paymentClient = client.order.create({'amount':dollarAmount*100*80, 'currency':'INR','payment_capture':'1' })
                
                payment_obj = Payment(user=user, currency=selectedCurrency, 
                    txId=paymentClient['id'], dollarAmount=dollarAmount,)
                payment_obj.save()

                request.session['payment_id'] = payment_obj.id
                request.session['dollarAmount'] = dollarAmount

                return render(request,'createtransaction.html',{'payment':paymentClient,'fund' : fund})        
        
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
    url = "https://test.cashfree.com/api/v1/order/create"

    payload={
        'appId': '102751a0cb37f516a65e6eed74157201',
        'secretKey': '5fe7a1a61683b7e10ba50413e019381091f72ef7',
        'orderId': 'order_00112',
        'orderAmount': '500',
        'orderCurrency': 'INR',
        'orderNote': 'Test order',
        'customerEmail': 'sample@gmail.com',
        'customerName': 'Cashfree User',
        'customerPhone': '9999999999',
        'returnUrl': 'http://localhost/handleResponse.php',
        'notifyUrl': 'http://localhost/handlePaymentStatus.php'
        }
    
    files=[
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    return render(request,'createorder.html')
