# Generated by Django 4.2.7 on 2023-11-28 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_order_item_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='drink',
            new_name='is_shoe',
        ),
    ]
