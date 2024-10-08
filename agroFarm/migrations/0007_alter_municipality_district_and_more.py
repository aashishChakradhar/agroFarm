# Generated by Django 4.2.14 on 2024-08-05 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agroFarm', '0006_country_municipality_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipality',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipalities', to='agroFarm.district'),
        ),
        migrations.AlterField(
            model_name='product',
            name='productType',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='agroFarm.producttype'),
        ),
    ]
