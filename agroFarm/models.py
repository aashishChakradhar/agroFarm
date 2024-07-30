from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator,validate_email
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

class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    streetName = models.CharField(max_length=20)
    landMark = models.CharField(max_length=20)
    postalCode = models.DecimalField(max_digits=6,decimal_places=0)
    default = models.BooleanField()
    def __str__(self):
        return self.country

class Product(BaseModel):
    sellerId = models.ForeignKey(User, on_delete=models.CASCADE,default=00)
    productName = models.CharField(max_length=30,default="unknown")
    productType = models.CharField(max_length=30,default="unknown")
    productDescription = models.CharField(max_length=100,default="unknown")
    productPrice = models.DecimalField(max_digits=5, decimal_places=2,default="unknown")

    def __str__(self):
        return self.productName
    
