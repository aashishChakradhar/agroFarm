# Generated by Django 4.2.14 on 2024-08-01 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agroFarm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productType',
            field=models.CharField(default='unknown', max_length=30),
        ),
    ]
