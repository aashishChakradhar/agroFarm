from django.contrib import admin
from django.urls import path,include
from agroFarm import views

urlpatterns = [
    #path("{urlpath}",{view class}, name="{reverse indexing}")
    path('', views.Index.as_view(), name='index'),
]