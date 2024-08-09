import paypalrestsdk
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages

paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

def create_paypal_payment(request, amount, description, return_url, cancel_url):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url,
        },
        "transactions": [
            {
                "amount": {
                    "total": amount,
                    "currency": "USD",
                },
                "description": description,
            }
        ],
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)  # Redirect to PayPal for payment
    return None
def execute_paypal_payment(request, success_url, failure_url):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    if not payment_id or not payer_id:
        return render(request, failure_url)

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        messages.success(request, 'Payment received successfully. Please check your PayPal account for confirmation.')
        return render(request, success_url)
    else:
        messages.error(request, 'Payment failed. Please try again.')
        return render(request, failure_url)