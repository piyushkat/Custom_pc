# Generated by Django 4.1.5 on 2023-02-01 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gaming_products', '0014_alter_allmodels_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allmodels',
            name='subcategory',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='gaming_products.subcategory'),
        ),
    ]
