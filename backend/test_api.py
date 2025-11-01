import requests
import json

# Test the products API endpoint
print("Testing GET /api/products endpoint...")
print("="*80)

try:
    # Assuming backend is running on localhost:8585
    response = requests.get("http://127.0.0.1:8585/api/products?limit=3")

    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])

        print(f"✅ API returned {len(products)} products\n")

        for product in products:
            print(f"Product: {product.get('name')}")
            print(f"  English Name: {product.get('englishName', 'MISSING FIELD!')}")
            print(f"  Category: {product.get('category')}")
            print(f"  Price: NT${product.get('price')}")
            print()

    else:
        print(f"❌ API returned status code: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("❌ Could not connect to backend API at http://127.0.0.1:8585")
    print("Make sure the backend server is running.")
except Exception as e:
    print(f"❌ Error: {e}")
