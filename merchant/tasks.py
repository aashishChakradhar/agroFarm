import requests
from merchant.models import Product, Product_User
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def fetch_and_store_data():
    logging.info("Starting API data fetch...")
    try:
        # Replace with your API endpoint
        response = requests.get("http://127.0.0.1:2000/veg", timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

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
            Product.objects.update_or_create(
                name=name,
                defaults={
                    'slug': slug,
                    'unit': unit,
                    'min_price': min_price,
                    'max_price': max_price,
                    'avg_price': avg_price,
                }
            )                
        
        # Fetch products from the database to display
        logging.info("API data fetched and stored successfully.")
    except requests.RequestException as e:
        logging.error(f"API fetch failed: {e}")