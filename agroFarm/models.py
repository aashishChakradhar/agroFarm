from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator
from datetime import date

# Create your models here.


class BaseModel(models.Model):
    uid = models.AutoField(primary_key=True, editable=False, unique=True)
    created = models.DateField(auto_now_add = True)
    modified = models.DateField(auto_now= True)
    class Meta:
        abstract = True

