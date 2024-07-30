from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# from datetime import date

# Create your models here.
class BaseModel(models.Model):
    uid = models.AutoField(primary_key=True, editable=False, unique=True)
    created = models.DateField(auto_now_add = True)
    modified = models.DateField(auto_now= True)
    class Meta:
        abstract = True


class BillingAddresss(BaseModel):
    country = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    streetName = models.CharField(max_length=20)
    landMark = models.CharField(max_length=20)
    postalCode = models.DecimalField(max_digits=6,decimal_places=0)
    phone_number = models.DecimalField(max_digits=10, decimal_places=0)


    

class Product(BaseModel):
    product_name = models.CharField(max_length=30)
    product_type = models.CharField(max_length=30)
    product_description = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=5, decimal_places=2)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.uid
    
