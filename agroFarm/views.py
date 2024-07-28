from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.template import loader
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse_lazy
from agroFarm.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class Index(View):
    def get(self, request):
        context = {
            "page_name":"Home"
        }
        return render(request,'index.html',context)
      
class Login_view(View):
    def get(self,request):
        alert_title = request.session.get('alert_title',False)
        alert_detail = request.session.get('alert_detail',False)
        if(alert_title):del(request.session['alert_title'])
        if(alert_detail):del(request.session['alert_detail'])
        context = {
            'alert_title': alert_title,
            'alert_detail': alert_detail,
            'page_name': 'Login'
        }
        return render(request,"login.html",context)
    
    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user is not None:# checks if the user is logged in or not?
            login(request,user) #logins the user
            return redirect ('/dashboard')
        else:
            request.session['alert_title'] = "Invalid Login Attempt"
            request.session['alert_detail'] = "Please enter valid login credential."
            return redirect(request.path)
        
class Logout_view(View):
    def get(self,request):
        request.session.clear()
        logout(request)
        return redirect('/')

#signup and login page ko lagi function from kiran
# @login_required(login_url = 'login')    
class Signup_View (View):
    def get(self,request):
        alert_title = request.session.get('alert_title',False)
        alert_detail = request.session.get('alert_detail',False)
        if(alert_title):del(request.session['alert_title'])
        if(alert_detail):del(request.session['alert_detail'])
        context = {
            'alert_title':alert_title,
            'alert_detail':alert_detail,
            'page_name': 'Signup'
        }
        return render(request,"signup.html",context)
        
    def post(self,request):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            #yeta email ko validation garnu parxa hola hai garbage value ma ni accept gari rakhya xa 
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if (password1 != password2):
                request.session['alert_title'] = "Invalid Password"
                request.session['alert_detail'] = "Password did not match."
                return redirect(request.path)
            else:
                user = User.objects.create_user(username = username, email=email, password=password1)
                user.save()
                user = authenticate(username = username, password = password1)
                if user is not None:# checks if the user is logged in or not?
                    login(request,user) #logins the user
                    return redirect ('/')          

class Dashboard_view(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/login')
        else:
            try:
                current_user = request.user
                context = {
                    'user' : current_user,
                    'page_name': 'Dashboard'
                }
                return render(request, "dashboard.html" ,context)
            except Exception as e:
                messages.error(request, str(e))
                return render(request,"dashboard.html")
            
class Account_dash_view(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/login')
        else:
            try:
                current_user = request.user
                context = {
                    'user' : current_user,
                    'page_name': 'My Account'
                }
                return render(request, "account-dashboard.html" ,context)
            except Exception as e:
                messages.error(request, str(e))
                return render(request,"account-dashboard.html")
            
class Product_dash_view(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/login')
        else:
            if request.user.is_superuser:
                products = Product.objects.all()
            else:
                products = Product.objects.filter(sellerid=request.user)
            
            try:
                context = {
                    'products' : products,
                    'page_name': 'Products'
                }
                return render(request, "product-dashboard.html" ,context)
            except Exception as e:
                messages.error(request, str(e))
                return render(request,"product-dashboard.html")