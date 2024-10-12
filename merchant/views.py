from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.urls import reverse

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

from merchant.models import *
# from static.pythonfiles.calculations import *

from django.http import JsonResponse

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect ('/merchant')
    
class Login(View):
    def get(self,request):
        context = {
            "page_name":"login",
        }
        return render(request,'merchant/login.html',context)
    
    def post (self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user is not None:# checks if the user is logged in or not?
            login(request,user) #logins the user
            return redirect('/merchant')
        else:
            messages.error(request, "You should check in on some of those fields below.")
            return redirect(request.path)

class BaseView(LoginRequiredMixin, View): #to check login or not
    login_url = '/merchant/login/'
    redirect_field_name = ''
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
            
    # pass

    
class Index(BaseView):
    def get(self, request):
        # if not request.user.is_authenticated:
        #     return render(request,'login.html')
        context = {
            "page_name":"home",
        }
        return render(request,'merchant/index.html',context)