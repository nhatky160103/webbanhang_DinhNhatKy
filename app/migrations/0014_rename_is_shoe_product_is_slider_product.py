# Generated by Django 4.2.7 on 2024-01-02 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_rename_product_orderitem_productvariant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_shoe',
            new_name='is_slider_product',
        ),
    ]