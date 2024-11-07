# from django.db import models
# from django.contrib.auth.models import User
# from phonenumber_field.modelfields import PhoneNumberField
# from datetime import date

from merchant.models import *

# Create your models here.
'''
class BaseModel(models.Model):
    uid = models.AutoField(primary_key=True, editable=False, unique=True)
    created = models.DateField(auto_now_add = True)
    modified = models.DateField(auto_now= True)
    class Meta:
        abstract = True

class ExtraDetails(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = PhoneNumberField()
    address = models.CharField(max_length=225, default='')
    def __str__(self):
        return self.user.username
   
class Country(BaseModel):
    name = models.CharField(max_length=30 ,default = "nepal")
    def __str__(self):
        return self.name

class Province(BaseModel):
    country = models.ForeignKey(Country,on_delete=models.CASCADE, related_name='provinces')
    name = models.CharField(max_length=30 ,default = "bagmati")
    def __str__(self):
        return self.name

class District(BaseModel):
    province = models.ForeignKey(Province,on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=30 ,default = "kathmandu")
    def __str__(self):
        return self.name

class BillingAddress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    municipality = models.CharField(max_length=30,default='unknown')
    street = models.CharField(max_length=30,default='unknown')
    postalCode = models.CharField(max_length=10,default='unknown')
    landmark = models.CharField(max_length=30,default='unknown')
    def __str__(self):
        return self.postalCode

    '''