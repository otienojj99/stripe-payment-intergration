from django.urls import path
from.import views
#app_name = 'payments'

urlpatterns = [
    path('', views.payment_checkout, name='payment_checkout'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('project_payment/', views.project_payment, name='project_payment'),
    path('execute_project_payment/', views.execute_project_payment, name='execute_project_payment'),
    path('project_checkout/', views.project_checkout, name='project_checkout'),
    path('club_payment/', views.club_payment, name='club_payment'),
    path('execute_club_payment/', views.execute_club_payment, name='execute_club_payment'),
    path('project_stripe_payment/', views.project_stripe_payment, name='project_stripe_payment'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('club_checkout/', views.club_checkout, name='club_checkout'),
    path('create_project_stripe_payment_intent/', views.create_project_stripe_payment_intent, name='create_project_stripe_payment_intent'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('execute-project-payment/', views.execute_project_payment, name='execute_project_payment'),
    path('club-stripe-payment/', views.club_stripe_payment, name='club_stripe_payment'),
    path('create-club-stripe-payment-intent/', views.create_club_stripe_payment_intent, name='create_club_stripe_payment_intent'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),

]