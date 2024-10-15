from django.contrib import admin
from .models import *

#  Register your models here.

admin.site.register(ExtraDetails)
admin.site.register(BillingAddress)

# for address
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(District)
# admin.site.register(Municipality)