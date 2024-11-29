from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse

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
        
        # Check if the user is a superuser or staff
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
        categorys = Category.objects.all()
        products = Product.objects.all()
        category = []
        for categories in categorys:
            # Check if there is any product that belongs to this category
            if categories.product_set.exists():  # product_set is the reverse relation for Category
                category_products = categories.product_set.all()[:4]  # [:4] limits to 4 products
                category.append({
                    'category': categories,
                    'products': category_products
                })
        context = {
            "page_name":"home",
            "rangelist" : [1,2,3,4] ,
            "categorys": category
        }
        return render(request,f'{app_name}/index.html',context)
    
    def post(self,request):
        action = request.POST.get('action')
        product_ids = request.POST.getlist('uid')
        print(product_ids)
        if action == 'buy':
            request.session['product_ids'] = product_ids  # Save IDs in session
            return redirect('customer:buy-now')
        # Default action (in case something goes wrong)
        return redirect(request.path)

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
            userID=request.user,
            country=country,
            state=province,
            district=district,
            municipality=municipality,
            zip_code=postalCode,
            street=street,
            landmark=landmark
        )
        address.save()
        return redirect ('/') 

class Product_Detail_View(BaseView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, uid=product_id)
        review = Review.objects.filter(productID = product)
        address = Address.objects.filter(userID = request.user)
        context = {
            "page_name": "product",
            "products": product,
            "reviews" : review,
            "address":address,
        }
        return render(request, f'{app_name}/product_detail.html', context)
    
    def post(self,request, product_id):
        action = request.POST.get('action')
        product_ids = request.POST.getlist('product_id')
        print(product_ids)
        if action == 'Buy Now':
            request.session['product_ids'] = product_ids  # Save IDs in session
            return redirect('customer:buy-now')
        elif action=='add to cart':
            return redirect(request.path)

        # Default action (in case something goes wrong)
        return redirect(request.path)

class BuyNowView(BaseView):
    def get(self, request):
        product_ids = request.session.get('product_ids', [])  # Retrieve product IDs from session

        if not product_ids:
            return redirect('customer:product-detail')  # Redirect back if no products are selected

        # Fetch all products matching the selected IDs
        products = Product.objects.filter(uid__in=product_ids)

        context = {
            "page_name": "buy-now",
            "products": products,
        }
        return render(request, f'{app_name}/buynow.html', context)
    
    def post(self, request):
        # Get all the product UIDs and quantities from the POST data
        product_uids = request.POST.getlist('cart_item')  # List of product UIDs
        quantities = request.POST.getlist('quantity')  # List of quantities

        # getting address of loged User
        address = Address.objects.get(userID = request.user)

        # Validate and process each product and its quantity
        if not product_uids or not quantities or len(product_uids) != len(quantities):
            messages.error(request, "Invalid data submitted", status=400)
            return redirect(request.path)

        orders = []  # List to store created order objects for further use or confirmation

        for product_uid, quantity_str in zip(product_uids, quantities):
            quantity = int(quantity_str)

            if quantity < 1:
                return HttpResponse('Quantity must be at least 1.', status=400)

            product = get_object_or_404(Product, uid=product_uid)
            total_price = product.rate * quantity

            # Create and save the order object
            order = Order.objects.create(
                userID=request.user,
                productID=product,
                addressID = address,
                quantity=quantity,
                rate=product.rate,
                amount=total_price
            )
            orders.append(order)
            OrderStatus.objects.create(
                orderID = order,
                is_pending = True,
                is_accepted=False,
                is_complete = False,
                is_cancelled=False,
            )

            # Delete the item from the cart after processing
            CartItem.objects.filter(user=request.user, product=product).delete()

        # Redirect to a confirmation or success page with relevant details
        messages.success(request, "Order has been placed")

        return redirect('customer:order-detail')

class AddToCartView(BaseView): #adds items to cart
    def get(self, request, product_uid):
        # Ensure the product exists
        product = get_object_or_404(Product, uid=product_uid)

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Please login to add products to your cart.'}, status=401)

        # Check if the product already exists in the cart
        cart_item = CartItem.objects.filter(user=request.user, product=product).first()
        if cart_item:
            print('already exissts')
            # Return "already in cart" response
            return JsonResponse({
                'success': False,
                'message': f'{product.name} is already in your cart.'
            }, status=400)

        # Add the product to the cart if it doesn't exist
        CartItem.objects.create(user=request.user, product=product)

        # Return success response
        return JsonResponse({
            'success': True,
            'message': f'{product.name} has been added to your cart.',
            'cart_count': CartItem.objects.filter(user=request.user).count(),
        })

class MyCart_View(BaseView): #show items in my cart
    def get(self, request):
        user = request.user

        # Get all cart items for the current user
        carts = CartItem.objects.filter(user=user)

        # Create a list to hold products corresponding to the cart items
        products = []

        # Loop through each cart item and get the related product
        for cart in carts:
            product = Product.objects.filter(name=cart.product).first()  # Use .first() to get one object or None
            if product:
                print(product.uid)  # Debug print statement
                products.append(product)  # Append the product to the list if it exists

        # Pass the full list of cart items and related products to the context
        context = {
            'page_name': 'my-cart',
            'carts': carts,
            'products': products,  # Pass the products to the template if needed
        }
        return render(request, f'{app_name}/cart.html', context)
    
    def post(self,request):
        action = request.POST.get('action')
        print(f"{action}:")

        # Get the list of selected product IDs from the POST data
        selected_product_ids = request.POST.getlist('cart_item')  # 'product' should match the name attribute of your checkboxes
        print("Selected product IDs:", selected_product_ids)

        products = []
        for uid in selected_product_ids:
            selected_products = Product.objects.filter(uid=uid).first()
            if selected_products:
                products.append(selected_products)  # Append the product to the list if it exists
        
        # Print the IDs for debugging (optional)
        productID_list = []
        for product in products:
            productID_list.append(product.uid)
            print(f"Product selected: {product.uid}")
        
        if action == 'delete':
            for product in products:
                print(f'objects deleted: {CartItem.objects.filter(user=request.user, product=product.uid).delete()}')
               
        elif action == 'buy':
            request.session['product_ids'] =  productID_list# Save IDs in session
            return redirect('customer:buy-now')
        return redirect(request.path)

class Order_Detail_View(View):
    def get(self,request):
        context = {
            'page_name' : 'myorder',
        }
        return render(request, f'{app_name}/order.html',context)
    def post(self,request):
        return redirect(request.path)

class Automate_Data_Entry(BaseView):
    def get(self,request):
        context = {
            'page_name' : 'automate-data',
            'app_name' : app_name,
        }
        automatic()
        return render(request,f"{app_name}/automate.html",context)
    def post(self,request):
        automatic()
        return redirect(request.path)
# class Add_Address(BaseView):
#     def get(self,request):
#         context = {
#             'page_name' : 'add-address',
#         }
#         return render(request, f"{app_name}/billing-address.html", context)

def search_product(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        results = Product.objects.filter(name__icontains=query) 
    return render(request, f'{app_name}/search.html', {'query': query, 'results': results})