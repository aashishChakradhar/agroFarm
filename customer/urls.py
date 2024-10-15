from django.contrib import admin
from django.urls import path,include
from customer import views

urlpatterns = [
    #path("{urlpath}",{view class}, name="{reverse indexing}")

    path('', views.Index.as_view(), name='home'),
    path('home/',views.Index.as_view(),name='home'),
    path('login/', views.Login_view.as_view(), name='login'),
    path('logout/', views.Logout_view.as_view(), name='logout'),
    path('signup/', views.Signup_View.as_view(), name='signup'),
    
]