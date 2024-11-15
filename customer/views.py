from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from customer.models import *
from merchant.models import *

from django.contrib.auth.mixins import LoginRequiredMixin
# from django.template import loader
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.decorators import login_required
# from django.urls import reverse_lazy

from myutility import *
from static.pythonFiles.automate_data_entry import automate_data_entry as automatic

app_name = 'customer'

class BaseView(LoginRequiredMixin, View): #to check login or not
    login_url = '/login/'
    redirect_field_name = ''

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'Please Login First')
            return redirect(self.login_url)  # Redirect to login if not authenticated
        
        # Check if the user is a superuser or staf
        if (request.user.is_superuser or request.user.is_staff):
            messages.error(request, 'Seems Like You Were in Wrong Portal')
            return redirect('merchant:login') # Redirect to the merchant login URL
        
        
        return super().dispatch(request, *args, **kwargs)

class Logout_view(BaseView):
    def get(self,request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')  # Add success message
        return redirect(reverse('customer:login'))  # Use reverse for URL resolution
           
class Login_view(View):
    def get(self,request):
        context = {
            'page_name': 'Login'
        }
        return render(request,f"{app_name}/login.html",context)
    
    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user is not None:# checks if the user is logged in or not?
            login(request,user) #logins the user
            return redirect ('/')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect(request.path)

class Signup_View (View):
    def get(self,request):
        context = {
            'page_name': 'signup'
        }
        return render(request,f"{app_name}/signup.html",context)
        
    def post(self,request):
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email') #validation required
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        mobile = request.POST.get('mobile')
        status = request.POST.get('status')

        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            messages.error(request,"Please enter valid email.")
            return redirect(request.path)
        
        # check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(request.path)
        
        #determine type of user
        if status == 'admin':
            is_superuser = True 
            is_staff = True
        elif status == 'merchant':
            is_superuser == False
            is_staff = True
        elif status =='customer':
            is_staff = False
            is_superuser = False

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect(request.path)
        
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.first_name = firstName
        user.last_name = lastName
        user.save()

        ExtraUserDetails.objects.create(userID=user, mobile=mobile)

        user = authenticate(username = username, password = password)
        if user is not None:# checks if the user is logged in or not?
            login(request,user) #logins the user
            return redirect('/')
        
        messages.error(request, "Error logging in. Please try again.")
        return redirect(request.path) 
            
class Index(BaseView):
    def get(self, request):
        context = {
            "page_name":"home"
        }
        return render(request,f'{app_name}/index.html',context)

class AddAddress_View(BaseView):
    def get(self,request):
        address_data = address()
        countrys = address_data['country']
        provinces = address_data['province']
        districts = address_data['district']
        context = {
            'page_name': 'billing-address',
            'countrys':countrys,
            'provinces':provinces,
            'districts':districts,

        }
        return render(request,f"{app_name}/add-address.html",context)

    def post(self,request):
        country = request.POST.get('country')
        province = request.POST.get('province')
        district = request.POST.get('district')
        municipality = request.POST.get('municipality')
        street = request.POST.get('street')
        postalCode = request.POST.get('postalCode')
        landmark = request.POST.get('landmark')

        # Fetch the related objects from the database

        address = Address.objects.create(
            country=country,
            state=province,
            district=district,
            # municipality=municipality,
            street=street,
            # postalCode=postalCode,
            # landmark=landmark
        )
        address.save()
        return redirect ('/') 

class Automate_Data_Entry(BaseView):
    def get(self,request):
        automatic()
        return redirect('/')

# class Add_Address(BaseView):
#     def get(self,request):
#         context = {
#             'page_name' : 'add-address',
#         }
#         return render(request, f"{app_name}/billing-address.html", context)