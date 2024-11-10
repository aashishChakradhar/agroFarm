from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class BaseModel(models.Model):
    uid = models.AutoField(primary_key=True, editable=False, unique=True)
    created = models.DateField(auto_now_add = True)
    modified = models.DateField(auto_now= True)
    class Meta:
        abstract = True

class Producttype(BaseModel):
    name = models.CharField(max_length=30, default='')
    featuredimage = models.CharField(max_length=1024, default='') 
    description = models.CharField(max_length=100, default='')
    def __str__(self):
        return self.name

class Product(BaseModel):
    sellerId = models.ForeignKey(User, on_delete=models.CASCADE,default=00)
    productName = models.CharField(max_length=30,default="unknown")
    productType = models.ManyToManyField(Producttype, default=0)
    featuredimage = models.CharField(max_length=1024, default='') 
    productDescription = models.CharField(max_length=100,default="unknown")
    productPrice = models.DecimalField(max_digits=5, decimal_places=2,default="unknown")

    def __str__(self):
        return self.productName
    
class Order(BaseModel):
    buyerId = models.ForeignKey(User, on_delete=models.CASCADE,default=00)
    product = models.ManyToManyField(Product, default=0)

    def __str__(self):
        return self.uid