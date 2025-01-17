from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Prefetch
from templatetags.product_data_fetcher import get_product_data
from datetime import datetime
import os

from .models import *
# from customer.models import ExtraDetails
# from static.pythonfiles.calculations import *

from django.http import JsonResponse

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin


from django.core.mail import send_mail
from django.conf import settings

def send_mail_to_customer(order):
    customer = get_object_or_404(User,id=order.userID_id)
    send_mail(
        f"Order ID : #{order.uid}",
        f"Your order for {order.productID} from {order.merchantID} is {order.status}.",
        settings.EMAIL_HOST_USER,
        [customer.email],
        fail_silently=False,
    )    

app_name = 'merchant'

class BaseView(LoginRequiredMixin, View):
    login_url = '/merchant/login/'
    redirect_field_name = ''
    
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'Please Login First')
            return redirect(self.login_url)
        
        # Check if the user is a superuser or staff
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, "Access Denied. Merchants only.")
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class Logout(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')  # Add success message
        return redirect(reverse('merchant:login'))  # Use reverse for URL resolution
    
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
            return redirect('/merchant/dashboard/')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect(request.path)

class SignupView (View):
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
            is_superuser = False
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
            return redirect('merchant:my-address')
        
        messages.error(request, "Error logging in. Please try again.")
        return redirect(request.path) 

class AddressView(BaseView):
    def get(self, request):
        if not Address.objects.exists():
            addrss = None
        else:
            # Check if the user has an address
            address = Address.objects.filter(userID=request.user).first()

        context = {
            'page_name': 'billing-address',
            'address': address,
        }
        return render(request, f"{app_name}/add-address.html", context)

# logical error
    def post(self,request):
        action = request.POST.get('action')
        country = request.POST.get('country')
        state = request.POST.get('province')
        district = request.POST.get('district')
        municipality = request.POST.get('municipality')
        street = request.POST.get('street')
        zip_code = request.POST.get('postalCode')
        landmark = request.POST.get('landmark')
        if action == 'edit':            
            # Fetch the related objects from the database
            address = Address.objects.get(userID = request.user)
            address = Address.objects.update(
                userID=request.user,
                country=country,
                state=state,
                district=district,
                municipality=municipality,
                zip_code=zip_code,
                street=street,
                landmark=landmark,
                is_deleted = False,
            )
        elif action == 'add':            
            address = Address.objects.create(
                userID=request.user,
                country=country,
                state=state,
                district=district,
                municipality=municipality,
                zip_code=zip_code,
                street=street,
                landmark=landmark,
                is_deleted = False,
            )
            address.save()
        return redirect ('/') 

class Index(BaseView):
    def get(self, request):
        context = {
            "page_name":"home",
        }
        return render(request,f'{app_name}/index.html',context)
    
# class AddProductView(BaseView):
#     def get(self, request):
#         try:
#             context = {
#                 'page_name': 'add-product'
#             }
#             return render(request, f"{app_name}/add_product.html" ,context)
#         except Exception as e:
#             messages.error(request, str(e))
#             return render(request,f"{app_name}/add_product.html")

#     def post(self,request):
#         try:
#             producttitle = request.POST.get('producttitle')
#             featuredimage = request.POST.get('productimgblob')
#             stock = request.POST.get('stock')
            
#             cat = request.POST.get('producttype')
#             description = request.POST.get('editorContent')
#             sellerid = request.user

#             category = get_object_or_404(Category, uid=cat)
#             price = category.avg_price
#             price = price.split(' ')[1]

#             if not producttitle or not price:
#                 messages.error(request, "All fields are required.")
#                 return render(request, f'{app_name}/add_product.html')
            
#             product = Product(
#                 name=producttitle,
#                 merchantID=sellerid,
#                 featuredimage=featuredimage,
#                 stock_quantity = stock,
#                 rate = price,
#                 description = description,
#                 categoryID = category
#             )
#             product.save()

#             messages.success(request, "Your Product Has Been Successfully Added!")
#             return redirect(request.path) 
        
#         except Exception as e:
#             messages.error(request, str(e))
      
#         return render(request, f'{app_name}/add_product.html') 

class ProductView(BaseView):
    def get(self, request):
        products = Product.objects.all().order_by('-created')
        # user_product = Product.objects.filter(product_user__userID=request.user).order_by('-created')
        for product in products:
            image_path = os.path.join('static/', 'images', f"{product.slug}.png")
            product.image_exists = os.path.isfile(image_path)
        
        try:
            context = {
                'products' : products,
                'page_name': 'products'
            }
            return render(request, f"{app_name}/product.html" ,context)
        except Exception as e:
            messages.error(request, str(e))
            return render(request,f"{app_name}/product.html")  
    
class DashboardView(BaseView):
    def get(self, request):
        user_product_ids = Product_User.objects.filter(userID=request.user).values_list('uid', flat=True)
        orders = Order.objects.filter(productID__in=user_product_ids)
        try:
            current_user = request.user
            context = {
                'orders' : orders,
                'user' : current_user,
                'page_name': 'Dashboard'
            }
            return render(request, f"{app_name}/dashboard.html" ,context)
        except Exception as e:
            messages.error(request, str(e))
            return render(request,f"{app_name}/dashboard.html")
               
class AccountView(BaseView):
    def get(self, request):
        try:
            current_user = request.user
            context = {
                'user' : current_user,
                'extrafields' : get_object_or_404(ExtraUserDetails, userID=current_user.id),
                'page_name': 'my-account'
            }
            return render(request, f"{app_name}/account.html" ,context)
        except Exception as e:
            messages.error(request, str(e))
            return render(request,f"{app_name}/account.html")
        
    def post(self,request):
        user = request.user

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        featuredimage = request.POST.get('profileimgblob') if request.POST.get('profileimgblob') else ''
        biotext = request.POST.get('biotext')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        try:
            # Update User fields
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            try:
                extrauserfields = ExtraUserDetails.objects.get(userID=user.id)
                extrauserfields.mobile=phone
                extrauserfields.profileimg=featuredimage
                extrauserfields.bio=biotext
                extrauserfields.latitude = latitude
                extrauserfields.longitude = longitude
                extrauserfields.save()
            except:
                ExtraUserDetails.objects.create(
                    userID=user, 
                    mobile=phone, 
                    profileimg=featuredimage, 
                    bio=biotext,
                    latitude = latitude,
                    longitude = longitude
                )

            messages.success(request, "Your profile has been successfully updated!")
            return redirect('/merchant/account/')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('/merchant/account/')
      
        return render(request, f'{app_name}/account.html') 
    
class OrderView(BaseView):
    def get(self,request):
        current_user = request.user
        user_product_ids = Product_User.objects.filter(userID=current_user.id).values_list('uid', flat=True)
        orders = Order.objects.filter(productID__in=user_product_ids)
        context = {
            'orders' : orders,
            'page_name':'order'
        }
        return render(request,f'{app_name}/order.html',context)
    
class EditProductView(BaseView):
    def get(self, request, id):
        try:
            product = get_object_or_404(Product, uid=id)
            min_price = product.min_price.split(' ')[1]
            max_price = product.max_price.split(' ')[1]
            image_path = os.path.join('static/', 'images', f"{product.slug}.png")
            image_exists = os.path.isfile(image_path)
            context = {
                'product' : get_object_or_404(Product, uid=id),
                'min_price': min_price,
                'max_price': max_price,
                'image_exists' : image_exists,
                'page_name': 'edit-product'
            }
            return render(request, f"{app_name}/edit_product.html" ,context)
        except Exception as e:
            messages.error(request, str(e))
            return render(request,f"{app_name}/edit_product.html")

    def post(self,request, id):
        try:
            price = request.POST.get('price')
            stock = request.POST.get('stock')

            if not stock or not price:
                messages.error(request, "All fields are required.")
                return render(request, f'{app_name}/edit_product.html')

            Product_User.objects.update_or_create(
                productID=Product.objects.get(uid=id), 
                userID=request.user,
                defaults={
                    'quantity' : stock,
                    'price':price,
                }
            )

            messages.success(request, "Your Product Has Been Updated!")
            return redirect('/merchant/products/edit-product/' + str(id))  # Redirect to a blog list or success page after editing
        
        except Exception as e:
            messages.error(request, str(e)) 
            return render(request,f"{app_name}/edit_product.html")

class DeleteProductView(View):
    def get(self, request, id):
        if request.user.is_anonymous:
            return redirect('/login')
        
        try:
            delobj = get_object_or_404(Product, uid=id)
            delobj.delete()
            messages.success(request, "Deletion Successful")
            return redirect('/merchant/products/')
        except Exception as e:
            messages.error(request, "Deletion Unsuccessful")
            return redirect('/merchant/products/')

class ProductTypeView(BaseView):
    def get(self, request):
        if request.user.is_superuser:
            category = Category.objects.all().order_by('-created')
        else:
            category = Category.objects.filter(merchantID=request.user).order_by('-created')
        
        try:
            context = {
                'categories' : category,
                'page_name': 'productcategory'
            }
            return render(request, f"{app_name}/producttype.html" ,context)
        except Exception as e:
            messages.error(request, str(e))
            return render(request,f"{app_name}/producttype.html")  
        
class EditOrderView(BaseView):
    def get(self, request, id):
        try:
            order = Order.objects.get(uid=id)
            context = {
                'order' : order,
                'address' : order.addressID,
                'page_name': 'edit-order'
            }
            return render(request, f"{app_name}/edit_order.html" ,context)
        except Exception as e:
            messages.error(request, str(e))
            return render(request,f"{app_name}/edit_order.html")

    def post(self,request, id):
        try:
            order = get_object_or_404(Order, uid=id)

            status = request.POST.get('orderstatus')
            
            order.status=status

            order.save()

            send_mail_to_customer(order)
            messages.success(request, "Your Order Has Been Updated!")
            return redirect('/merchant/order/edit-order/' + str(id))  # Redirect to a blog list or success page after editing
        
        except Exception as e:
            messages.error(request, str(e)) 
            return render(request,f"{app_name}/edit_order.html")
        
#can be removed        
class FetchedProductView(BaseView):
    def get(self, request):
        data = get_product_data()
        
        # Handle error case
        if isinstance(data, str):
            return render(request, 'error.html', {'error': data})
        
        # Save each product in the database
        for x in data:
            name = data[x]['name']
            unit = data[x]['unit']
            min_price = data[x]['min']
            max_price = data[x]['max']
            avg_price = data[x]['avg']
            
            # Check if the product exists; if not, create or update it
            Category.objects.update_or_create(
                name=name,
                defaults={
                    'unit': unit,
                    'min_price': min_price,
                    'max_price': max_price,
                    'avg_price': avg_price,
                }
            )
        
        # Fetch products from the database to display
        products = Product.objects.all()
        
        return render(request, f'{app_name}/test_fetchproduct.html', {'products': products})