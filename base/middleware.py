from django.shortcuts import redirect
from .models import CustomUser

class AppointmentRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('appointment_token')
        if token and not request.path.startswith('/booking/'):
            try:
                appointment = CustomUser.objects.get(token=token)
                if appointment:
                    if appointment.is_paid:
                        response = redirect('main-dashboard', token=appointment.token)
                        return response
                    else:
                        return redirect('stripe-payment',pk=appointment.id)
                else:
                    return redirect('dashboard')
            except CustomUser.DoesNotExist:
                pass
        response = self.get_response(request)
        return response