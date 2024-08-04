from django.contrib import admin
from agroFarm.models import *

#  Register your models here.

admin.site.register(Product)
admin.site.register(Producttype)
admin.site.register(BillingAddress)

# for address
admin.site.register(Country)
admin.site.register(District)
admin.site.register(Municipality)