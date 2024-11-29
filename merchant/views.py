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

from .models import *
# from customer.models import ExtraDetails
# from static.pythonfiles.calculations import *

from django.http import JsonResponse

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

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
            return redirect('/merchant')
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
            return redirect('/')
        
        messages.error(request, "Error logging in. Please try again.")
        return redirect(request.path) 

class Index(BaseView):
    def get(self, request):
        context = {
            "page_name":"home",
        }
        return render(request,f'{app_name}/index.html',context)
    
class AddProductView(BaseView):
    def get(self, request):
        try:
            context = {
                'categories': Category.objects.all() ,
                'page_name': 'add-product'
            }
            return render(request, f"{app_name}/add_product.html" ,context)
        except Exception as e:
            messages.error(request, str(e))
            return render(request,f"{app_name}/add_product.html")

    def post(self,request):
        try:
            producttitle = request.POST.get('producttitle')
            featuredimage = request.POST.get('productimgblob')
            print(featuredimage)
            price = request.POST.get('price')
            cat = request.POST.getlist('producttype')
            description = request.POST.get('editorContent')
            sellerid = request.user

            types = []
            for x in cat:
                try:
                    product_type = Category.objects.get(name=x)
                    types.append(product_type)
                except Category.DoesNotExist:
                    messages.error(request, f"Product type '{x}' does not exist.")
                    return render(request, f'{app_name}/add_product.html')

            if not producttitle or not price:
                messages.error(request, "All fields are required.")
                return render(request, f'{app_name}/add_product.html')
            
            product = Product(
                name=producttitle,
                merchantID=sellerid,
                featuredimage=featuredimage,
                rate = price,
                description = description
            )
            product.save()

            product.categoryID.set(types)

            messages.success(request, "Your Product Has Been Successfully Added!")
            return redirect(request.path) 
        
        except Exception as e:
            messages.error(request, str(e))
      
        return render(request, f'{app_name}/add_product.html') 

class ProductView(BaseView):
    def get(self, request):
        if request.user.is_superuser:
            products = Product.objects.all().order_by('-created')
        else:
            products = Product.objects.filter(sellerId=request.user).order_by('-created')
        
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
        if request.user.is_superuser:
            orders = Order.objects.all().order_by('-created')
        else:
            orders = Order.objects.filter(sellerId=request.user).order_by('-created')

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
                extrauserfields.save()
            except:
                ExtraUserDetails.objects.create(
                    userID=user, 
                    mobile=phone, 
                    profileimg=featuredimage, 
                    bio=biotext
                )

            messages.success(request, "Your profile has been successfully updated!")
            return redirect('/merchant/account/')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('/merchant/account/')
      
        return render(request, f'{app_name}/account.html') 
    
class OrderView(BaseView):
    def get(self,request):
        orders = Order.objects.all().order_by('-created')
        # if request.user.is_superuser:
        #     orders = Order.objects.all().order_by('-created')
        # else:
        #     orders = Order.objects.filter(sellerId=request.user).order_by('-created')
        context = {
            'order' : orders,
            'page_name':'order'
        }
        return render(request,f'{app_name}/order.html',context)
    
class EditProductView(BaseView):
    def get(self, request, id):
        try:
            context = {
                'product' : get_object_or_404(Product, uid=id),
                'categories': Category.objects.all() ,
                'page_name': 'edit-product'
            }
            return render(request, f"{app_name}/edit_product.html" ,context)
        except Exception as e:
            messages.error(request, str(e))
            return render(request,f"{app_name}/edit_product.html")

    def post(self,request, id):
        try:
            product = get_object_or_404(Product, uid=id)

            producttitle = request.POST.get('producttitle')
            featuredimage = request.POST.get('productimgblob')
            price = request.POST.get('price')
            cat = request.POST.getlist('producttype')
            description = request.POST.get('editorContent')

            types = []
            for x in cat:
                try:
                    product_type = Category.objects.get(name=x)
                    types.append(product_type)
                except Category.DoesNotExist:
                    messages.error(request, f"Product type '{x}' does not exist.")
                    return render(request, f'{app_name}/edit_product.html')

            if not producttitle or not price:
                messages.error(request, "All fields are required.")
                return render(request, f'{app_name}/edit_product.html')
            
            product.name=producttitle
            product.featuredimage=featuredimage
            product.rate = price
            product.description = description

            product.save()

            product.categoryID.set(types)

            messages.success(request, "Your Product Has Been Updated!")
            return redirect('/merchant/products/edit-product/' + str(id))  # Redirect to a blog list or success page after editing
        
        except Exception as e:
            messages.error(request, str(e)) 

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

class AddProductTypeView(BaseView):
    def get(self, request):
        try:
            context = {
                'categories': Category.objects.all() ,
                'page_name': 'add-producttype'
            }
            return render(request, f"{app_name}/add_producttype.html" ,context)
        except Exception as e:
            messages.error(request, str(e))
            return render(request,f"{app_name}/add_producttype.html")

    def post(self,request):
        try:
            categorytitle = request.POST.get('producttypetitle')
            featuredimage = request.POST.get('producttypeimgblob')
            description = request.POST.get('editorContent')
            merchantID = request.user
            
            if not categorytitle:
                messages.error(request, "All fields are required.")
                return render(request, f'{app_name}/add_producttype.html')
            
            producttype = Category(
                merchantID=merchantID,
                name=categorytitle,
                featuredimage=featuredimage,
                description = description
            )
            producttype.save()

            messages.success(request, "The Category Has Been Successfully Added!")
            return redirect(request.path) 
        
        except Exception as e:
            messages.error(request, str(e))
      
        return render(request, f'{app_name}/add_producttype.html') 
    
class EditProductTypeView(BaseView):
    def get(self, request, id):
        try:
            context = {
                'category' : get_object_or_404(Category, uid=id),
                'page_name': 'edit-product'
            }
            return render(request, f"{app_name}/edit_producttype.html" ,context)
        except Exception as e:
            messages.error(request, str(e))
            return render(request,f"{app_name}/edit_producttype.html")

    def post(self,request, id):
        try:
            category = get_object_or_404(Category, uid=id)

            producttitle = request.POST.get('producttypetitle')
            featuredimage = request.POST.get('producttypeimgblob')
            description = request.POST.get('editorContent')
            
            category.name=producttitle
            category.featuredimage=featuredimage
            category.description = description

            category.save()

            messages.success(request, "Your Category Has Been Updated!")
            return redirect('/merchant/products/edit-producttype/' + str(id))  # Redirect to a blog list or success page after editing
        
        except Exception as e:
            messages.error(request, str(e)) 
            return render(request,f"{app_name}/edit_product.html")

class DeleteCategoryView(View):
    def get(self, request, id):
        if request.user.is_anonymous:
            return redirect('/login')
        
        try:
            delobj = get_object_or_404(Category, uid=id)
            delobj.delete()
            messages.success(request, "Deletion Successful")
            return redirect('/merchant/products/producttype/')
        except Exception as e:
            messages.error(request, "Deletion Unsuccessful")
            return redirect('/merchant/products/producttype/')