from django.contrib import admin
from django.urls import path,include
from customer import views

urlpatterns = [
    # path("{urlpath}",{view class}, name="{reverse indexing}")
    # name should remain unchanged
    # links references to name

    path('', views.Index.as_view(), name='home'),
    path('home/',views.Index.as_view(),name='home'),
    path('login/', views.Login_view.as_view(), name='login'),
    path('logout/', views.Logout_view.as_view(), name='logout'),
    path('signup/', views.Signup_View.as_view(), name='signup'),
    path('add-address/', views.AddAddress_View.as_view(), name='add-address'),
    path('order-detail/', views.Order_Detail_View.as_view(), name='order-detail'),
    path('my-cart/', views.Cart_View.as_view(), name='my-cart'),
    path('add-data/', views.Automate_Data_Entry.as_view(), name='add-data'),
    path('product-detail/<int:product_id>/', views.Product_Detail_View.as_view(), name='product-detail'),
    path('add-to-cart/<int:product_uid>/', views.AddToCartView.as_view(), name='add-to-cart'),

]