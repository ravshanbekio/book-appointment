from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import date
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

class InitialForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['type_of_visa',]

        labels = {
            'type_of_visa':'',
        }

        widgets = {
            'type_of_visa':forms.Select(attrs={'type':"text", 'name':"name", 'placeholder':"Name", 'data-form-field':"name", 'class':"form-control", 'value':"", 'id':"name-form02-i"}),
        }

class AppointmentDateTimeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['appointment_date','appointment_time']

        labels = {
            'appointment_date':'',
            'appointment_time':'',
        }

        widgets = {
            'appointment_date': forms.DateInput(attrs={'type':'date','placeholder':'Select appointment date','class':'form-control'}),
            'appointment_time': forms.Select(attrs={'type':'select','placeholder':'Select appointment time','class':'form-control'}),
        }
    
    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        appointment_time = self.cleaned_data.get('appointment_time')
        if appointment_date < date.today():
            self.add_error('appointment_date','The selected date cannot be in the past.')
        elif CustomUser.objects.filter(appointment_date=appointment_date, appointment_time=appointment_time).exists():
            self.add_error('appointment_date',f'The selected date {appointment_date} is already booked. Please choose another date.')
        return appointment_date
    
    def clean_appointment_time(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        appointment_time = self.cleaned_data.get('appointment_time')
        if CustomUser.objects.filter(appointment_date=appointment_date, appointment_time=appointment_time).exists():
            self.add_error('appointment_time',f'The selected time at {appointment_time} is already booked. Please choose another time.')
        return appointment_time
            
class RemainFieldsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name','date_of_birth','nationality','passport_number','current_city','email','phone_number']

        labels = {
            'full_name':'',
            'date_of_birth':'',
            'nationality':'',
            'passport_number':'',
            'current_city':'',
            'email':'',
            'phone_number':'',
        }

        widgets = {
            'full_name': forms.TextInput(attrs={'type':'text','placeholder':'Full name','class':'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type':'date','placeholder':'Date of birth','class':'form-control'}),
            'nationality': forms.Select(attrs={'type':'select','placeholder':'Select your country','class':'form-control'}),
            'passport_number': forms.TextInput(attrs={'type':'text','placeholder':'Passport number','class':'form-control'}),
            'current_city': forms.Select(attrs={'type':'select','placeholder':'Select your current city/region','class':'form-control','name':'current_city'}),
            'email': forms.EmailInput(attrs={'type':'email','placeholder':'Email address','class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'type':'text','placeholder':'Phone number','class':'form-control'}),
        }

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name) < 5:
            self.add_error('full_name', "Full name must be at least 5 characters long.")
        return full_name

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        if age < 18:
            self.add_error('date_of_birth', "You must be at least 18 years old.")
        return date_of_birth
    
    def clean_passport_number(self):
        passport_number = self.cleaned_data.get('passport_number')
        if CustomUser.objects.filter(passport_number=passport_number).exists():
            self.add_error('passport_number', "This Passport number is already registered")
        return passport_number
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            self.add_error('email', "This Email address is already registered")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            self.add_error('phone_number', "This phone_number is already registered")
        return phone_number