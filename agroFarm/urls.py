from django.contrib import admin
from django.urls import path,include
from agroFarm import views

urlpatterns = [
    #path("{urlpath}",{view class}, name="{reverse indexing}")

    path('', views.Index.as_view(), name='home'),
    path('index',views.Index.as_view(),name='home'),
    path('login', views.Login_view.as_view(), name='login'),
    path('logout', views.Logout_view.as_view(), name='logout'),
    path('signup', views.Signup_View.as_view(), name='signup'),
    path('billing-address', views.BillingAddress_View.as_view(), name='billing-address'),#on working phase
    path('dashboard', views.Dashboard_view.as_view(), name='dashboard'),
    path('dashboard/account', views.Account_dash_view.as_view(), name='Account'),
    path('dashboard/products', views.Product_dash_view.as_view(), name='Products'),
    path('dashboard/products/add-new', views.Add_product_view.as_view(), name='Add Products'),
    path('dashboard/products/edit-product/<int:id>', views.Edit_product_view.as_view(), name='Edit Products'),
]