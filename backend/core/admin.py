from django.contrib import admin
from .models import Product, Inventory, Sale, SaleItem, Negotiation, PriceHistory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'list_price')
    search_fields = ('name', 'sku')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'qty')
    search_fields = ('product__name',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'cashier', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'qty', 'unit_price')
    search_fields = ('sale__id', 'product__name')

@admin.register(Negotiation)
class NegotiationAdmin(admin.ModelAdmin):
    list_display = ('product', 'proposed_price', 'status', 'proposer', 'created_at')
    list_filter = ('status',)
    search_fields = ('product__name', 'proposer')

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'new_price', 'old_price', 'changed_at')
    search_fields = ('product__name',)

