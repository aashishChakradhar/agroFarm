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
from merchant import views
from django.urls import path,include


'''
    namespace is assigned for dynamic routing
'''

app_name = 'merchant'

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('home/', views.Index.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('my-address/', views.AddressView.as_view(), name='my-address'),
    # path('products/add-new/', views.AddProductView.as_view(), name='add-products'),#for merchant
    path('products/edit-product/<int:id>', views.EditProductView.as_view(), name='edit-products'),#for merchant
    path('products/delete-product/<int:id>', views.DeleteProductView.as_view(), name="delete-product"),
    path('products/producttype/', views.ProductTypeView.as_view(), name='producttype'),#for merchant
    # path('products/add-producttype/', views.AddProductTypeView.as_view(), name='add-producttype'),#for merchant
    # path('products/edit-producttype/<int:id>', views.EditProductTypeView.as_view(), name='edit-producttype'),#for merchant
    # path('products/delete-producttype/<int:id>', views.DeleteCategoryView.as_view(), name="delete-producttype"),
    path('products/', views.ProductView.as_view(), name='products'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('order/edit-order/<int:id>', views.EditOrderView.as_view(), name='edit-order'),
    path('fetch-products/', views.FetchedProductView.as_view(), name='fetch-product'),
    # path('edit-product/<int:id>', views.EditProductView.as_view(), name='edit-products'),#for merchant

    # path('billing-address', views.BillingAddress_View.as_view(), name='billing-address'),#on working phase
]       
