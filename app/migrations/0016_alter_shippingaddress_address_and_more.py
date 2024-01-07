# Generated by Django 4.2.7 on 2024-01-06 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_shippingaddress_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='email',
            field=models.EmailField(max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='phone_number',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='street',
            field=models.CharField(max_length=200),
        ),
    ]
