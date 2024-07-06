from django import forms

class StripePaymentForm(forms.Form):
    pass  # No fields needed as we will handle this via Stripe.js
