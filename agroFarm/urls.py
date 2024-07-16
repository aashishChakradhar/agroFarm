from django.contrib import admin
from django.urls import path,include
from agroFarm import views

urlpatterns = [
    #path("{urlpath}",{view class}, name="{reverse indexing}")
    path('', views.Index.as_view(), name='home'),
    path('index',views.Index.as_view(),name='home'),
    path('login', views.Login_view.as_view(), name='login'),
]