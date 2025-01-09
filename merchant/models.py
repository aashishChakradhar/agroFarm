from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from customer.models import *

# Create your models here.

class BaseModel(models.Model):
    uid = models.AutoField(primary_key=True, editable=False, unique=True)
    created = models.DateField(auto_now_add = True)
    modified = models.DateField(auto_now= True)
    class Meta:
        abstract = True

class Address(BaseModel):
    userID = models.OneToOneField(User,on_delete=models.CASCADE,default=1)
    country = models.CharField(max_length=50, default='Unknown')
    state  = models.CharField(max_length=50, default='Unknown')
    district = models.CharField(max_length=50, default='Unknown')
    municipality = models.CharField(max_length=50, default='Unknown')
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, default='Unknown')
    landmark = models.CharField(max_length=100,default='Unknown')
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.street}, {self.municipality}, {self.district}, {self.state}, {self.country}"

class ExtraUserDetails(BaseModel):
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = PhoneNumberField()
    profileimg = models.CharField(max_length=1024, default='') 
    bio = models.CharField(max_length=1024, default='') 
    # addressID = models.OneToOneField(Address,on_delete=models.CASCADE, default=0)
    def __str__(self):
        return self.user.username


class Category(BaseModel):
    merchantID = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50, default='')
    unit = models.CharField(max_length=30, default='')
    min_price = models.CharField(max_length=30, default='')
    max_price = models.CharField(max_length=30, default='')
    avg_price = models.CharField(max_length=30, default='')
    def __str__(self):
        return self.name

class Tag(BaseModel):
    title = models.CharField(max_length=30, default='')
    def __str__(self):
        return self.title

class Product(BaseModel):
    merchantID = models.ForeignKey(User, on_delete=models.CASCADE,default=00)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE, default=00)
    tagID = models.ManyToManyField(Tag)
    name = models.CharField(max_length=30,default="unknown")
    featuredimage = models.CharField(max_length=1024, default='') 
    description = models.TextField(default="unknown")
    rate = models.DecimalField(max_digits=5, decimal_places=2,default="unknown")
    stock_quantity = models.PositiveIntegerField(default=1)
    stock_available = models.PositiveIntegerField(default=1)
    review_count = models.PositiveIntegerField(default=0)
    review_average = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name

# class Product_Tag(BaseModel):
#     tagID = models.ForeignKey(Tag, on_delete=models.CASCADE)
#     produtID = models.ForeignKey(Product, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.title
    
class Review(BaseModel):
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    productID = models.ForeignKey(Product,on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    comment = models.TextField(default="")
    def __str__(self):
        return f'Rating: {self.rating} for Product: {self.productID.name} by User: {self.userID.username}'

class Store(BaseModel):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    addressID = models.ForeignKey(Address, on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=50, default='Unknown')
    pan = models.CharField(max_length=15, default='Unknown')
    def __str__(self):
        return self.name

class OrderAddress(BaseModel):
    country = models.CharField(max_length=50, default='Unknown')
    state  = models.CharField(max_length=50, default='Unknown')
    district = models.CharField(max_length=50, default='Unknown')
    municipality = models.CharField(max_length=50, default='Unknown')
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, default='Unknown')
    landmark = models.CharField(max_length=100,default='Unknown')

    def __str__(self):
        return f"{self.street}, {self.municipality}, {self.district}, {self.state}, {self.country}"

class Order(BaseModel):
    merchantID = models.ForeignKey(User,on_delete=models.CASCADE,related_name='merchant_transactions',default = 1) 
    userID = models.ForeignKey(User, on_delete=models.CASCADE,related_name='buyer_transactions') #buyer ID
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    addressID = models.ForeignKey(OrderAddress, on_delete=models.CASCADE,default=0)
    quantity = models.PositiveIntegerField(default=1)  # Changed to store whole numbers
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=50, default='processing')

    def __str__(self):
        return str(self.uid)

class PaymentMethod(BaseModel):
    orderID = models.ForeignKey(Order,on_delete=models.CASCADE)
    is_cashOnDelivery = models.BooleanField(default='True')
    is_online = models.BooleanField(default='False')
    def __str__(self):
        return self.orderID
    
class CartItem(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f'{self.user} added {self.product} to cart'