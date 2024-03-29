# Generated by Django 3.0.5 on 2020-08-17 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('initial_quantity', models.IntegerField(null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('price', models.FloatField(blank=0.0, default=0.0, verbose_name='Cost Price')),
                ('cost_price', models.FloatField(blank=0.0, default=0.0, verbose_name='Selling Price')),
                ('initial_discount', models.FloatField(blank=0.0, default=0.0, null=True)),
                ('gst', models.FloatField(blank=0.0, default=0.0, null=True)),
                ('transport_charge', models.FloatField(blank=0.0, default=0.0, null=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='items.ItemModel')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
    ]
