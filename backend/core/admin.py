from django.contrib import admin
from .models import Product, Inventory, Sale, SaleItem, Negotiation, PriceHistory
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Negotiation)
admin.site.register(PriceHistory)
