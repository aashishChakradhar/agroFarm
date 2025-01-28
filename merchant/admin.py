from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Address)
admin.site.register(ExtraUserDetails)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Store)
admin.site.register(Order)
admin.site.register(Product_User)
admin.site.register(PaymentMethod)