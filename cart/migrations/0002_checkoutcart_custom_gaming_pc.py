# Generated by Django 4.1.5 on 2023-02-03 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gaming_products', '__first__'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkoutcart',
            name='custom_gaming_pc',
            field=models.ManyToManyField(related_name='custom_gaming', to='gaming_products.customgamingpc'),
        ),
    ]
