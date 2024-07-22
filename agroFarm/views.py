from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.template import loader
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from agroFarm.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class Index(View):
    def get(self, request):
        context = {
            "page_name":"home"
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
            'page_name': 'login'
        }
        return render(request,"login.html",context)
    
    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user is not None:# checks if the user is logged in or not?
            login(request,user) #logins the user
            return redirect ('/')
        else:
            request.session['alert_title'] = "Invalid Login Attempt"
            request.session['alert_detail'] = "Please enter valid login credential."
            return redirect(request.path)
        
class Logout_view(View):
    def get(self,request):
        request.session.clear()
        logout(request)
        return redirect('/')

def dashboardpageloader(request):
  context = {
    'page_name': 'Dashboard'
  }
  return render(request, "dashboard.html" ,context)


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
            'page_name': 'signup'
        }
        return render(request,"signup.html",context)
        
    def post(self,request):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
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