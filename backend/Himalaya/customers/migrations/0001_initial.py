# Generated by Django 3.0.5 on 2020-08-17 07:49

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50, null=True)),
                ('lname', models.CharField(max_length=50, null=True)),
                ('mobile', models.CharField(max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('birth_day', models.DateField(blank=True, null=True)),
                ('date', models.DateField(blank=True, default=datetime.date(2020, 8, 17), null=True)),
            ],
        ),
    ]
