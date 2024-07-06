from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from base.models import CustomUser

class Command(BaseCommand):
    help = 'Delete incomplete appointments older than 24 hours'

    def handle(self, *args, **kwargs):
        expiration_time = timezone.now() - timedelta(hours=24)
        incomplete_appointments = CustomUser.objects.filter(is_got_appointment=False, appointment_updated_at__lt=expiration_time)
        count = incomplete_appointments.count()
        incomplete_appointments.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} incomplete appointments older than 24 hours'))
