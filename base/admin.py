from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("full_name", "email", "nationality","is_got_appointment",)
    list_filter = ("email","is_got_appointment","passport_number", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("full_name", "nationality","current_city","date_of_birth",)}),
        ("Private information", {"fields": ("passport_number","phone_number")}),
        ("Booking proccess", {"fields": ("type_of_visa","appointment_date","appointment_time","is_paid","is_reviewed", "is_got_appointment")}),
        ("Permissions", {"fields": ("token","is_staff", "is_active",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("-email",)


admin.site.register(CustomUser, CustomUserAdmin)