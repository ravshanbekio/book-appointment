# Generated by Django 5.0.6 on 2024-06-20 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_customuser_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='address',
        ),
    ]
