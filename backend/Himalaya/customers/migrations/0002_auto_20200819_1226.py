# Generated by Django 3.0.5 on 2020-08-19 06:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2020, 8, 19), null=True),
        ),
    ]
