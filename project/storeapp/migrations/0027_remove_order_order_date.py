# Generated by Django 4.2.4 on 2023-10-04 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0026_product_batch_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_date',
        ),
    ]
