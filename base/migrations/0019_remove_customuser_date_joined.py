# Generated by Django 5.0.6 on 2024-06-21 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_customuser_is_reviewed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='date_joined',
        ),
    ]
