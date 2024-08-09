from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from agroFarm.models import *
from agroFarm.form import SignupForm

# from django.template import loader
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.decorators import login_required
# from django.urls import reverse_lazy

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
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            username = request.POST.get('username')
            email = request.POST.get('email') #validation required
            password = request.POST.get('password')
            status = request.POST.get('status')

            #determine type of user
            if status == 'admin':
                is_superuser = True 
                is_staff = True
            elif status == 'seller':
                is_superuser == False
                is_staff = True
            elif status =='customer':
                is_staff = False
                is_superuser = False

                
            user = User.objects.create_user(username , email, password,is_superuser=is_superuser,is_staff = is_staff)
            user.save()

            #additional user details
            user.first_name=firstName
            user.last_name=lastName
            user.save()
            user = authenticate(username = username, password = password)
            if user is not None:# checks if the user is logged in or not?
                login(request,user) #logins the user
            return redirect ('/')          

class BillingAddress(View):
    def get(self,request):
        alert_title = request.session.get('alert_title',False)
        alert_detail = request.session.get('alert_detail',False)
        if(alert_title):del(request.session['alert_title'])
        if(alert_detail):del(request.session['alert_detail'])
        # not sure how it works
        # in trial phase
        country = Country.objects.all()
        province = Province.objects.all()
        district = District.objects.all()
        municipality = Municipality.objects.all()


        context = {
            'alert_title':alert_title,
            'alert_detail':alert_detail,
            'page_name': 'billing-address',
            'country':country,
            'province':province,
            'district':district,
            'municipality':municipality,

        }
        return render(request,"billing-address.html",context)
    
    def post(self,request):
        if request.method == 'POST':
            #thinking of creating a seperate database for storing districts and the municipalities within themselves
            #for dynamic rendering the form
            #the values are passed through context
            if User.is_authenticated and User.is_staff and not User.is_superuser:
                country = request.POST.get('country')
                province = request.POST.get('province')
                district = request.POST.get('district')
                municipality = request.POST.get('municipality')
                street = request.POST.get('street')
                postalCode = request.POST.get('postalCode')
                landmark = request.POST.get('landmark')
                billingAddress = BillingAddress(
                    country=country,
                    province=province,
                    district=district,
                    municipality=municipality,
                    street=street,
                    postalCode=postalCode,
                    landmark=landmark,
                )
                billingAddress.save()
            else:
                request.session['alert_title'] = "Unauthorized Login"
                request.session['alert_detail'] = "Please login through valid account"
                return redirect('agroFarm:login')
        return redirect ('/') 


class Dashboard_view(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/login')
        
        if request.user.is_superuser or request.user.is_staff:
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
        
        messages.error(request, 'Access Denied')
        return redirect('/')
            
class Account_dash_view(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/login')
        
        if request.user.is_superuser or request.user.is_staff:
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
            
        messages.error(request, 'Access Denied')
        return redirect('/')
            
class Product_dash_view(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/login')
        
        if request.user.is_superuser or request.user.is_staff:
            if request.user.is_superuser:
                products = Product.objects.all().order_by('-created')
            else:
                products = Product.objects.filter(sellerId=request.user).order_by('-created')
            
            try:
                context = {
                    'products' : products,
                    'page_name': 'Products'
                }
                return render(request, "product-dashboard.html" ,context)
            except Exception as e:
                messages.error(request, str(e))
                return render(request,"product-dashboard.html")
            
        messages.error(request, 'Access Denied')
        return redirect('/')
            
class Add_product_view(View):
    def get(self, request):
        if request.user.is_anonymous:
            return redirect('/login')
        
        if request.user.is_superuser or request.user.is_staff:
            try:
                context = {
                    'categories': Producttype.objects.all() ,
                    'page_name': 'Add Products'
                }
                return render(request, "add-product-dashboard.html" ,context)
            except Exception as e:
                messages.error(request, str(e))
                return render(request,"add-product-dashboard.html")
            
        messages.error(request, 'Access Denied')
        return redirect('/')

    def post(self,request):
        if request.method == 'POST':
            try:
                producttitle = request.POST.get('producttitle')
                featuredimage = request.FILES.get('featuredimage')
                price = request.POST.get('price')
                cat = request.POST.getlist('producttype')
                description = request.POST.get('editorContent')
                sellerid = request.user

                types = []
                for x in cat:
                    try:
                        product_type = Producttype.objects.get(name=x)
                        types.append(product_type)
                    except Producttype.DoesNotExist:
                        messages.error(request, f"Product type '{x}' does not exist.")
                        return render(request, 'add-product-dashboard.html')

                if not producttitle or not price:
                    messages.error(request, "All fields are required.")
                    return render(request, 'add-product-dashboard.html')
                
                product = Product(
                    productName=producttitle,
                    sellerId=sellerid,
                    featuredimage=featuredimage,
                    productPrice = price,
                    productDescription = description
                )
                product.save()

                product.productType.set(types)

                messages.success(request, "Your Blog Has Been Successfully Added!")
                return redirect('/dashboard/products/add-new')  # Redirect to a blog list or success page after adding
            
            except Exception as e:
                messages.error(request, str(e))
      
        return render(request, 'add-product-dashboard.html')   
    
class Edit_product_view(View):
    def get(self, request, id):
        if request.user.is_anonymous:
            return redirect('/login')
        
        if request.user.is_superuser or request.user.is_staff:
            try:
                context = {
                    'product' : get_object_or_404(Product, uid=id),
                    'categories': Producttype.objects.all() ,
                    'page_name': 'Edit Products'
                }
                return render(request, "edit-product-dashboard.html" ,context)
            except Exception as e:
                messages.error(request, str(e))
                return render(request,"edit-product-dashboard.html")
            
        messages.error(request, 'Access Denied')
        return redirect('/')

    def post(self,request, id):
        if request.method == 'POST':
            try:
                product = get_object_or_404(Product, uid=id)

                producttitle = request.POST.get('producttitle')
                featuredimage = request.FILES.get('featuredimage')
                price = request.POST.get('price')
                cat = request.POST.getlist('producttype')
                description = request.POST.get('editorContent')

                types = []
                for x in cat:
                    try:
                        product_type = Producttype.objects.get(name=x)
                        types.append(product_type)
                    except Producttype.DoesNotExist:
                        messages.error(request, f"Product type '{x}' does not exist.")
                        return render(request, 'edit-product-dashboard.html')

                if not producttitle or not price:
                    messages.error(request, "All fields are required.")
                    return render(request, 'edit-product-dashboard.html')
                
                product.productName=producttitle
                product.featuredimage=featuredimage
                product.productPrice = price
                product.productDescription = description

                product.save()

                product.productType.set(types)

                messages.success(request, "Your Blog Has Been Successfully edited!")
                return redirect('/dashboard/products/edit-product/' + str(id))  # Redirect to a blog list or success page after editing
            
            except Exception as e:
                messages.error(request, str(e))
      
        return render(request, 'edit-product-dashboard.html')   