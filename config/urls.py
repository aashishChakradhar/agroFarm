"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include


admin.site.site_header = "AgroFarm Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "AgroFarm"


'''
    namespace is assigned for dynamic routing
'''

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'), #app for admin page
    path('',include(('agroFarm.urls','agroFarm'),namespace = 'agroFarm')), # app for customer page
    path('merchant/',include(('merchant.urls','merchant'),namespace = 'merchant')), # app for seller page
]
