from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from agroFarm.models import *

class Index(View):
    def get(self, request):
        return render(request,'index.html')
        