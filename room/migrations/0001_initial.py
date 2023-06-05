# Generated by Django 4.2.1 on 2023-06-04 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('focus', 'Focus'), ('team', 'Team'), ('conference', 'Conference')], max_length=30)),
                ('capacity', models.PositiveIntegerField()),
            ],
        ),
    ]
