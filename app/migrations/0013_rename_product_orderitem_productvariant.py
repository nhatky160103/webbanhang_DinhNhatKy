# Generated by Django 4.2.7 on 2024-01-02 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_color_size_remove_product_price_product_price_avg_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='product',
            new_name='productvariant',
        ),
    ]
