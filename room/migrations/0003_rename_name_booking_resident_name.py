# Generated by Django 4.2.1 on 2023-06-05 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_booking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='name',
            new_name='resident_name',
        ),
    ]