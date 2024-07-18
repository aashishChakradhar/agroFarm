from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator
from datetime import date
from django.contrib.auth import User


# Create your models here.
class BaseModel(models.Model):
    uid = models.AutoField(primary_key=True, editable=False, unique=True)
    created = models.DateField(auto_now_add = True)
    modified = models.DateField(auto_now= True)
    class Meta:
        abstract = True


    

class Product(BaseModel):
    product_name = models.CharField()
    product_type = models.CharField()
    product_price = models.DecimalField(_max_digits=5, decimal_places=2)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.uid
    
