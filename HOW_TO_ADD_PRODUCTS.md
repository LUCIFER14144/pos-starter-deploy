# 🛍️ How to Add Products to Your POS System

## 🎯 **Quick Start - 3 Easy Methods**

### **Method 1: 🖥️ Django Admin Panel (Recommended for Beginners)**

**✅ Your Django server should be running at: http://127.0.0.1:8000/**

1. **Access Admin Panel:**
   - Go to: **http://127.0.0.1:8000/admin/**
   - Username: `admin`
   - Password: [the password you created]

2. **Add Products:**
   - Click **"Products"** → **"Add Product"**
   - Fill in:
     - **SKU:** `ITEM001` (unique identifier - like a barcode)
     - **Name:** `Coffee`
     - **Cost Price:** `2.50` (what you paid for it)
     - **List Price:** `5.00` (selling price)
   - Click **"Save"**

3. **Add Inventory:**
   - Click **"Inventorys"** → **"Add Inventory"**
   - Select your product
   - Set **Qty:** `100` (how many you have in stock)
   - Click **"Save"**

---

### **Method 2: 🚀 Management Commands (Fastest for Bulk)**

Open a **new terminal** and run these commands:

```bash
# Go to the backend folder
cd backend

# Option A: Add sample products for testing
python manage.py add_products --sample

# Option B: Add products from CSV file
python manage.py add_products --csv ../sample_products.csv

# Option C: Add products interactively (one by one)
python manage.py add_products --interactive
```

---

### **Method 3: 🔧 API Endpoint (For Developers)**

Your backend has a REST API endpoint:

**POST** `http://localhost:8000/api/products/create/`

```json
{
    "sku": "COFFEE001",
    "name": "Premium Coffee", 
    "cost_price": 2.50,
    "list_price": 5.00,
    "qty": 100
}
```

---

## 📋 **Product Fields Explained**

| Field | Description | Example |
|-------|-------------|---------|
| **SKU** | Unique identifier (like barcode) | `COFFEE001` |
| **Name** | Product display name | `Premium Coffee` |
| **Cost Price** | What you paid for it | `$2.50` |
| **List Price** | Selling price | `$5.00` |
| **Qty** | Stock quantity | `100` |

---

## 🎮 **Testing Your Setup**

1. **Backend:** http://127.0.0.1:8000/admin/
2. **Frontend:** http://localhost:3000/ 
3. **API:** http://127.0.0.1:8000/api/products/

The frontend will automatically show your products in the POS interface!

---

## 📁 **CSV Import Format**

Create a file called `products.csv`:

```csv
sku,name,cost_price,list_price,qty
COFFEE001,Premium Coffee,2.50,5.00,100
TEA001,Green Tea,1.50,3.00,75
SNACK001,Chocolate Bar,1.00,2.50,200
```

Then import: `python manage.py add_products --csv products.csv`

---

## 🛠️ **Troubleshooting**

**Problem:** Django server not running
- **Solution:** Run `python manage.py runserver` in the `backend/` folder

**Problem:** Frontend not showing products
- **Solution:** Check that both servers are running (Django on port 8000, React on port 3000)

**Problem:** "Product already exists" error
- **Solution:** Each SKU must be unique. Use a different SKU or check existing products in admin panel

---

## ✨ **Ready to Sell!**

Once you've added products using any method above:

1. **Open POS:** http://localhost:3000/
2. **Scan/Enter SKU:** Type `COFFEE001` 
3. **Add to Cart:** Click "Add to Cart"
4. **Checkout:** Process the sale

Your POS system is now fully functional! 🎉