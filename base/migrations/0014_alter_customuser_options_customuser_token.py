# Generated by Django 5.0.6 on 2024-06-19 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={},
        ),
        migrations.AddField(
            model_name='customuser',
            name='token',
            field=models.CharField(default=8652, max_length=5),
        ),
    ]
