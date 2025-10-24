// Example: Add products via API using JavaScript/curl

// Using JavaScript (fetch)
fetch('http://localhost:8000/api/products/create/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        sku: 'COFFEE001',
        name: 'Premium Coffee',
        cost_price: 2.50,
        list_price: 5.00,
        qty: 100  // Initial inventory
    })
});

// Using curl command
curl -X POST http://localhost:8000/api/products/create/ \
  -H "Content-Type: application/json" \
  -d '{"sku":"COFFEE001","name":"Premium Coffee","cost_price":2.50,"list_price":5.00,"qty":100}'

// Sample products to add:
const sampleProducts = [
    {
        sku: 'COFFEE001',
        name: 'Premium Coffee',
        cost_price: 2.50,
        list_price: 5.00,
        qty: 100
    },
    {
        sku: 'TEA001',
        name: 'Green Tea',
        cost_price: 1.50,
        list_price: 3.00,
        qty: 75
    },
    {
        sku: 'SNACK001',
        name: 'Chocolate Bar',
        cost_price: 1.00,
        list_price: 2.50,
        qty: 200
    },
    {
        sku: 'WATER001',
        name: 'Bottled Water',
        cost_price: 0.50,
        list_price: 1.50,
        qty: 300
    }
];