import json
from django.conf import settings
import paypalrestsdk
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.shortcuts import  redirect
from django.urls import reverse
from django.contrib import messages
from .serializers import create_paypal_payment,execute_paypal_payment


def create_payment(request):
     return_url = request.build_absolute_uri(reverse('execute_payment'))
     cancel_url = request.build_absolute_uri(reverse('payment_cancelled'))
     amount = "1"
     description = "Payment for Product/Service"
     
     return create_paypal_payment(request, amount, description, return_url, cancel_url) or redirect('payments')
@csrf_exempt
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    if not payment_id or not payer_id:
        messages.error(request, 'Payment failed. Please try again.')
        return render(request, 'failedpay.html')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        messages.success(request, 'Payment received successfully. Please check your PayPal account for confirmation.')
        return render(request,'success.html')  # Redirect to home after displaying the success message
    else:
        messages.error(request, 'Payment failed. Please try again.')
        return render(request, 'failedpay.html')
    
def payment_checkout(request):
    return render(request, 'base.html')    

def project_payment(request):
    return_url = request.build_absolute_uri(reverse('execute_project_payment'))
    cancel_url = request.build_absolute_uri(reverse('payment_cancelled'))
    amount = "2"
    description = "Payment for Project/Service"
    
    return create_paypal_payment(request, amount, description, return_url, cancel_url) or redirect('payments')

@csrf_exempt
def execute_project_payment(request):
    return execute_paypal_payment(request, 'success.html', 'failedpay.html')

def club_payment(request):
    return_url = request.build_absolute_uri(reverse('execute_club_payment'))
    cancel_url = request.build_absolute_uri(reverse('payment_cancelled'))
    amount = "2"
    description = "Payment for Club Membership"
    
    return create_paypal_payment(request, amount, description, return_url, cancel_url) or redirect('payments')

@csrf_exempt
def execute_club_payment(request):
   return execute_paypal_payment(request, 'success.html', 'failedpay.html')

def project_checkout(request):
    return render(request, 'base1.html')

def club_checkout(request):
    return render(request, 'base1.html')

def payment_cancelled(request):
   return render(request, 'cancelled.html')


stripe.api_key = settings.STRIPE_SECRET_KEY
# Stripe for Project
@csrf_exempt
def project_stripe_payment(request): 
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'base.html', context)

@csrf_exempt
def create_project_stripe_payment_intent(request):
    domain = "http://127.0.0.1:8000"
    if request.method == 'POST':
         try:
             data = json.loads(request.body)
             payment_method_id = data['payment_method']
             email = data.get('email')
             country = data.get('country')
             save_details = data.get('save_details')
             full_name = data.get('full_name')
             

            
             intent = stripe.PaymentIntent.create(
                    amount=1049700,  # Amount in cents
                    currency='usd',
                    payment_method=payment_method_id,
                    confirmation_method='manual',
                    confirm=True,
                    return_url= domain + '/payment_checkout/',
                     metadata={
                    'country': country,
                    'save_details': save_details  # Store checkbox value in metadata
                },
                )
             return JsonResponse({'client_secret': intent.client_secret})
         except stripe.error.CardError as e:
           return JsonResponse({'error': 'Something went wrong. Please try again later.'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400) 

# Stripe for Club
def club_stripe_payment(request):
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'base1.html', context)

@csrf_exempt
def create_club_stripe_payment_intent(request):
    domain = "http://127.0.0.1:8000"
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_method_id = data['payment_method']
            email = data.get('email')
            country = data.get('country')
            save_details = data.get('save_details')
            full_name = data.get('full_name')

            intent = stripe.PaymentIntent.create(
                amount=149500,  # Amount in cents ($1495.00)
                currency='usd',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                return_url= domain + '/payment_checkout/',
                 metadata={
                    'country': country,
                    'save_details': save_details  # Store checkbox value in metadata
                },
                
            )
            return JsonResponse({'client_secret': intent.client_secret})
        except stripe.error.CardError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
def payment_success(request):
    messages.success(request, 'Payment received successfully.')
    return redirect('payment_checkout')
def payment_cancelled(request):
    return render(request, 'cancelled.html')  
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        # Fulfill the purchase, mark payment as complete in your database, etc.
        print('PaymentIntent was successful!')
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
        # Handle successful attachment of a PaymentMethod
        print('PaymentMethod was attached to a Customer!')
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event['type']))

    return JsonResponse({'status': 'success'})