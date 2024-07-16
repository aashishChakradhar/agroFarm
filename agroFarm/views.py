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
    
def dashboardpageloader(request):
  template = loader.get_template('dashboard.html')
  return HttpResponse(template.render())
        