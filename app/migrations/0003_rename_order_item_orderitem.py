# Generated by Django 4.2.7 on 2023-11-05 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_product_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order_item',
            new_name='OrderItem',
        ),
    ]
