# Generated by Django 3.0.5 on 2020-08-17 07:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brands', '0001_initial'),
        ('payment', '0001_initial'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_discount', models.FloatField(blank=0.0, default=0.0, null=True)),
                ('total_amount', models.FloatField(blank=0.0, default=0.0, null=True)),
                ('amount_payable', models.FloatField(blank=0.0, default=0.0, null=True)),
                ('receipt_pdf', models.FileField(blank=True, null=True, upload_to='')),
                ('date_time', models.DateTimeField(default=datetime.datetime(2020, 8, 17, 13, 19, 20, 18128), null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.Customer')),
                ('payment_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.PaymentModel')),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(default='', max_length=20)),
                ('quantity', models.IntegerField(default=1, null=True)),
                ('selling_price', models.FloatField(blank=0.0, default=0.0, null=True)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='brands.BrandModel')),
                ('receipt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='receipts.Receipts')),
            ],
        ),
    ]
