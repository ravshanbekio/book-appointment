from celery import shared_task
from django.core.management import call_command

@shared_task
def delete_incomplete_appointments_task():
    call_command('delete_incomplete_appointments')
