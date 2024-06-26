# Generated by Django 4.2.4 on 2023-09-25 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0021_rename_quantity_product_quantity_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand_name',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity_prefix',
            field=models.CharField(choices=[('gms', 'gms'), ('kg', 'kg')], default='gms', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity_value',
            field=models.PositiveIntegerField(default=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
    ]
