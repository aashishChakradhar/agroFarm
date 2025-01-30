import requests
from merchant.models import Product, Product_User
import logging
from datetime import datetime
from django.shortcuts import get_object_or_404

logging.basicConfig(level=logging.INFO)

def fetch_and_store_data():
    logging.info("Starting API data fetch...")
    try:
        # Replace with your API endpoint
        response = requests.get("http://127.0.0.1:2000/veg", timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        products_list = []

        # Parse and process the data
        data = response.json()  # Assuming the API returns JSON data
        for x in data:
            slug = x
            name = data[x]['name']
            unit = data[x]['unit']
            min_price = data[x]['min']
            max_price = data[x]['max']
            avg_price = data[x]['avg']
            
            # Check if the product exists; if not, create or update it
            products_list.append(Product.objects.update_or_create(
                name=name,
                defaults={
                    'slug': slug,
                    'unit': unit,
                    'min_price': min_price,
                    'max_price': max_price,
                    'avg_price': avg_price,
                }
            ))

        for product in products_list:
            p = Product_User.objects.filter(productID=product[0].uid)
            for item in p:  # Iterate over each item in the queryset
                if(item.price < float((product[0].min_price).split('Rs')[1])):
                    item.price = float((product[0].min_price).split('Rs')[1])
                elif(item.price > float((product[0].max_price).split('Rs')[1])):
                    item.price = float((product[0].max_price).split('Rs')[1])
            
                item.save()
        
        # Fetch products from the database to display
        logging.info("API data fetched and stored successfully.")
    except requests.RequestException as e:
        logging.error(f"API fetch failed: {e}")