# Generated by Django 4.2.4 on 2023-10-04 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0029_alter_product_quantity_prefix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity_prefix',
            field=models.CharField(choices=[('gms', 'gms'), ('kg', 'kg')], default='gms', max_length=10),
        ),
    ]
