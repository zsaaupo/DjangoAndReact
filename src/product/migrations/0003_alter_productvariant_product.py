# Generated by Django 3.2.8 on 2023-12-29 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_productvariantprice_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_variant', to='product.product'),
        ),
    ]
