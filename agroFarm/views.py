from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.template import loader
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from agroFarm.models import *

class Index(View):
    def get(self, request):
        return render(request,'index.html')
      
class Login_view(View):
    def get(self,request):
        alert_title = request.session.get('alert_title',False)
        alert_detail = request.session.get('alert_detail',False)
        if(alert_title):del(request.session['alert_title'])
        if(alert_detail):del(request.session['alert_detail'])
        context = {'alert_title':alert_title,
            'alert_detail':alert_detail,}
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
  template = loader.get_template('dashboard.html')
  return HttpResponse(template.render())


#signup and login page ko lagi function from kiran
# @login_required(login_url = 'login')      
def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if (password1 != password2):
            return HttpResponse("Your password and confirm password doesn't match.")
        else:
            my_user = User.objects.create_user(username, email, password1)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method = 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, usename = usename, password = password)
        if user is not None:
            login(request, user)
            customer = user.usename
            return redirect('dashboard.') 
        else:
            return redirect('signup')
        
    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')