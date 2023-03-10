# Generated by Django 4.1.5 on 2023-02-04 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gaming_products', '__first__'),
        ('cart', '0003_alter_checkoutcart_custom_gaming_pc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutcart',
            name='cart',
            field=models.ManyToManyField(blank=True, related_name='cart', to='gaming_products.allmodels'),
        ),
        migrations.AlterField(
            model_name='checkoutcart',
            name='custom_gaming_pc',
            field=models.ManyToManyField(blank=True, related_name='custom_gaming', to='gaming_products.customgamingpc'),
        ),
    ]
