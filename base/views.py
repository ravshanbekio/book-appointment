from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.conf import settings
from .forms import InitialForm, AppointmentDateTimeForm, RemainFieldsForm
from .models import CustomUser
from payments.models import UserPayment
import random
import stripe

CITY_EMAIL_MAPPING = {
    'Berlin': 'ravshanbekrm06@gmail.com',
    'Hamburg': 'aboutjohndoe77@gmail.com',
    'Munich': 'munich-immigration@example.com',
    'Cologne': 'cologne-immigration@example.com',
    'Frankfurt': 'frankfurt-immigration@example.com',
    'Stuttgart': 'stuttgart-immigration@example.com',
    'Düsseldorf': 'dusseldorf-immigration@example.com',
    'Dortmund': 'dortmund-immigration@example.com',
    'Essen': 'essen-immigration@example.com',
    'Leipzig': 'leipzig-immigration@example.com',
    'Bremen': 'bremen-immigration@example.com',
    'Dresden': 'dresden-immigration@example.com',
    'Hanover': 'hanover-immigration@example.com',
    'Nuremberg': 'nuremberg-immigration@example.com',
    'Duisburg': 'duisburg-immigration@example.com',
    'Bochum': 'bochum-immigration@example.com',
    'Wuppertal': 'wuppertal-immigration@example.com',
    'Bielefeld': 'bielefeld-immigration@example.com',
    'Bonn': 'bonn-immigration@example.com',
    'Münster': 'munster-immigration@example.com',
    'Karlsruhe': 'karlsruhe-immigration@example.com',
    'Mannheim': 'mannheim-immigration@example.com',
    'Augsburg': 'augsburg-immigration@example.com',
    'Wiesbaden': 'wiesbaden-immigration@example.com',
    'Gelsenkirchen': 'gelsenkirchen-immigration@example.com',
    'Mönchengladbach': 'moenchengladbach-immigration@example.com',
    'Braunschweig': 'braunschweig-immigration@example.com',
    'Chemnitz': 'chemnitz-immigration@example.com',
    'Kiel': 'kiel-immigration@example.com',
    'Aachen': 'aachen-immigration@example.com',
    'Halle': 'halle-immigration@example.com',
    'Magdeburg': 'magdeburg-immigration@example.com',
    'Freiburg': 'freiburg-immigration@example.com',
    'Krefeld': 'krefeld-immigration@example.com',
    'Lübeck': 'luebeck-immigration@example.com',
    'Oberhausen': 'oberhausen-immigration@example.com',
    'Erfurt': 'erfurt-immigration@example.com',
    'Mainz': 'mainz-immigration@example.com',
    'Rostock': 'rostock-immigration@example.com',
    'Kassel': 'kassel-immigration@example.com',
    'Hagen': 'hagen-immigration@example.com',
    'Saarbrücken': 'saarbruecken-immigration@example.com',
    'Hamm': 'hamm-immigration@example.com',
    'Mülheim': 'muelheim-immigration@example.com',
    'Potsdam': 'potsdam-immigration@example.com',
    'Ludwigshafen': 'ludwigshafen-immigration@example.com',
    'Oldenburg': 'oldenburg-immigration@example.com',
    'Leverkusen': 'leverkusen-immigration@example.com',
    'Osnabrück': 'osnabrueck-immigration@example.com',
    'Solingen': 'solingen-immigration@example.com',
    'Heidelberg': 'heidelberg-immigration@example.com',
    'Herne': 'herne-immigration@example.com',
    'Neuss': 'neuss-immigration@example.com',
    'Darmstadt': 'darmstadt-immigration@example.com',
    'Paderborn': 'paderborn-immigration@example.com',
    'Regensburg': 'regensburg-immigration@example.com',
    'Ingolstadt': 'ingolstadt-immigration@example.com',
    'Würzburg': 'wuerzburg-immigration@example.com',
    'Wolfsburg': 'wolfsburg-immigration@example.com',
    'Offenbach': 'offenbach-immigration@example.com',
    'Ulm': 'ulm-immigration@example.com',
    'Heilbronn': 'heilbronn-immigration@example.com',
    'Pforzheim': 'pforzheim-immigration@example.com',
    'Göttingen': 'goettingen-immigration@example.com',
    'Bottrop': 'bottrop-immigration@example.com',
    'Trier': 'trier-immigration@example.com',
    'Recklinghausen': 'recklinghausen-immigration@example.com',
    'Reutlingen': 'reutlingen-immigration@example.com',
    'Bremerhaven': 'bremerhaven-immigration@example.com',
    'Koblenz': 'koblenz-immigration@example.com',
    'Bergisch Gladbach': 'bergisch-gladbach-immigration@example.com',
    'Jena': 'jena-immigration@example.com',
    'Remscheid': 'remscheid-immigration@example.com',
    'Erlangen': 'erlangen-immigration@example.com',
    'Moers': 'moers-immigration@example.com',
    'Siegen': 'siegen-immigration@example.com',
    'Hildesheim': 'hildesheim-immigration@example.com',
    'Salzgitter': 'salzgitter-immigration@example.com',
}

class DashboardView(View):
    def get(self, request):
        return render(request, 'index.html')

class SelectDirectionView(View):
    def get(self, request):
        form = InitialForm()
        return render(request, 'choose_direction.html', {'form': form})

    def post(self, request):
        form = InitialForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            #Generate new token and save it as a cookie
            token = str(random.randint(11111,99999))
            appointment.token = token
            appointment.save()
            response = redirect('selecting-datetime', token=appointment.token)
            response.set_cookie('appointment_token', token, max_age=60*60*24*30)  # 30 days
            return response
        return redirect('selecting-direction')

class SelectDateTimeView(View):
    def get(self, request, token):
        form = AppointmentDateTimeForm()
        return render(request, 'select_datetime.html', {'form': form})

    def post(self, request, token):
        appointment = get_object_or_404(CustomUser, token=token)
        form = AppointmentDateTimeForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('user-details', token=appointment.token)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, error)
        return redirect('selecting-datetime', token=appointment.token)

class UserDetailsView(View):
    def get(self, request, token):
        form = RemainFieldsForm()
        stripe.api_key = settings.STRIPE_SECRET_KEY
        return render(request, 'user_details.html', {'form': form})

    def post(self, request, token):
        appointment = get_object_or_404(CustomUser, token=token)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        form = RemainFieldsForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            authenticate(request, email=form.cleaned_data.get('email'),password=form.cleaned_data.get('phone_number'))
            city = request.POST.get('current_city')
            recipient_email = None
            cities = list(CITY_EMAIL_MAPPING.keys())
            i = 0

            while i < len(cities):
                if cities[i] == city:
                    recipient_email = CITY_EMAIL_MAPPING[city]
                    break
                i += 1

            if not recipient_email:
                # Handle case where city is not in the mapping
                print("No email found for the specified city.")
                return redirect('dashboard')
            
            # Sending email to government
            subject = f'Appointment Request Submission - {appointment.full_name}'
            context = {
                'full_name': appointment.full_name,
                'date_of_birth': appointment.date_of_birth,
                'nationality': appointment.nationality,
                'passport_number': appointment.passport_number,
                'email': appointment.email,
                'phone_number': appointment.phone_number,
                'address': city,    
                'visa_type': appointment.type_of_visa,
                'appointment_date': appointment.appointment_date,
                'appointment_time': appointment.appointment_time,
                'official_name': f'{city} government',
                'organization_name': 'Appoint',
                'contact_information': 'ravshanbekmadaminov68@gmail.com'
            }
            message = render_to_string('appointment_request_email.html', context)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [recipient_email]
        
            email = EmailMessage(subject, message, email_from, recipient_list)
            email.content_subtype = 'html'
            email.send()

            # Sending email to the user
            user_subject = 'Thank You for Booking Your Appointment'
            user_context = {
                'full_name': appointment.full_name,
                'appointment_date': appointment.appointment_date,
                'appointment_time': appointment.appointment_time,
                'message': 'Your appointment is under review. We will notify you once it is confirmed.'
            }
            user_message = render_to_string('user_appointment_confirmation_email.html', user_context)
            user_email = EmailMessage(user_subject, user_message, settings.EMAIL_HOST_USER, [appointment.email])
            user_email.content_subtype = 'html'
            user_email.send()
            #Stripe payments
            if request.method == 'POST':
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types = ['card'],
                    line_items = [
                        {
                            'price': settings.PRODUCT_PRICE,
                            'quantity': 1,
                        },
                    ],
                    mode = 'payment',
                    customer_creation = 'always',
                    success_url = settings.REDIRECT_DOMAIN + f'/booking/{appointment.token}/success/',
                    cancel_url = settings.REDIRECT_DOMAIN + '/payments/cancelled/',
                )
                return redirect(checkout_session.url, code=303)
            
            return redirect('user_details',token=appointment.token)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, error)
        return redirect('user-details', token=appointment.token)

class MainDashboardView(View):
    def get(self, request, token):
        appointment = get_object_or_404(CustomUser, token=token)
        UserPayment.objects.create(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # checkout_session_id = request.GET.get('session_id', None)
        # session = stripe.checkout.Session.retrieve(checkout_session_id)
        # customer = stripe.Customer.retrieve(session.customer)
        # user_id = request.user.id
        # user_payment = UserPayment.objects.get(user=user_id)
        # user_payment.stripe_checkout_id = checkout_session_id
        # user_payment.save()

        appointment.is_paid = True
        appointment.save()
        return render(request, 'dashboard.html', {'appointment': appointment})