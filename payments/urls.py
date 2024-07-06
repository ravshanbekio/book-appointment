from django.urls import path
from . import views

urlpatterns = [
	path('cancelled/', views.payment_cancelled, name='payment_cancelled'),
	path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]