from django.db import models
from tinymce.models import HTMLField
from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class BaseModel(models.Model):
    uid = models.AutoField(primary_key=True, editable=False, unique=True)
    created = models.DateField(auto_now_add = True)
    modified = models.DateField(auto_now= True)
    class Meta:
        abstract = True

class Category(BaseModel):
  name = models.CharField(max_length=30)
  content = HTMLField(default = '')
  featuredimage = models.ImageField(upload_to='uploads/', default=0) 
  author = models.ForeignKey(User, on_delete=models.CASCADE, default='')

  def __str__(self):
    return f'{self.name}'

class Product(BaseModel):
    product_name = models.CharField(max_length=50, default='')
    featuredimage = models.ImageField(upload_to='uploads/', default=0)
    sellerid = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    product_price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=1)

    def __str__(self):
        return f'{self.title}'