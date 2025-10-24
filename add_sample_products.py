#!/usr/bin/env python3
"""
Sample script to add products to the POS system via API
Run this after starting the Django server (python manage.py runserver)
"""

import requests
import json

# API endpoint
BASE_URL = 'http://localhost:8000/api'

# Sample products to add
sample_products = [
    {
        'sku': 'COFFEE001',
        'name': 'Premium Coffee',
        'cost_price': 2.50,
        'list_price': 5.00,
        'qty': 100
    },
    {
        'sku': 'TEA001', 
        'name': 'Green Tea',
        'cost_price': 1.50,
        'list_price': 3.00,
        'qty': 75
    },
    {
        'sku': 'SNACK001',
        'name': 'Chocolate Bar', 
        'cost_price': 1.00,
        'list_price': 2.50,
        'qty': 200
    },
    {
        'sku': 'WATER001',
        'name': 'Bottled Water',
        'cost_price': 0.50,
        'list_price': 1.50,
        'qty': 300
    },
    {
        'sku': 'SANDWICH001',
        'name': 'Ham Sandwich',
        'cost_price': 3.00,
        'list_price': 7.50,
        'qty': 50
    }
]

def add_products():
    """Add sample products via API"""
    print("Adding sample products to POS system...")
    
    for product in sample_products:
        try:
            response = requests.post(
                f'{BASE_URL}/products/create/',
                headers={'Content-Type': 'application/json'},
                json=product
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Added: {product['name']} (ID: {result['id']})")
            else:
                print(f"❌ Failed to add {product['name']}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: Cannot connect to Django server.")
            print("Make sure the server is running: python manage.py runserver")
            return
        except Exception as e:
            print(f"❌ Error adding {product['name']}: {str(e)}")
    
    print(f"\n🎉 Finished! Added {len(sample_products)} products.")
    print("You can now use the POS frontend to see these products.")

if __name__ == "__main__":
    add_products()