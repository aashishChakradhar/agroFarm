# Generated by Django 4.2.14 on 2024-08-03 17:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agroFarm', '0004_producttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('uid', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('country', models.CharField(default='unknown', max_length=30)),
                ('province', models.CharField(default='unknown', max_length=30)),
                ('district', models.CharField(default='unknown', max_length=30)),
                ('municipality', models.CharField(default='unknown', max_length=30)),
                ('street', models.CharField(default='unknown', max_length=30)),
                ('postalCode', models.DecimalField(decimal_places=0, default='unknown', max_digits=30)),
                ('landmark', models.CharField(default='unknown', max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='ExtendedUser',
        ),
    ]
