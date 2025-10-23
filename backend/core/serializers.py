from rest_framework import serializers
from .models import Product, Inventory, Sale, SaleItem, Negotiation

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['product','qty']

class ProductSerializer(serializers.ModelSerializer):
    inventory = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','sku','name','cost_price','list_price','inventory']
    def get_inventory(self, obj):
        inv = getattr(obj, 'inventory', None)
        return inv.qty if inv else 0

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['product','qty','unit_price','line_total']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    class Meta:
        model = Sale
        fields = ['id','created_at','cashier','total','items']

class NegotiationSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = Negotiation
        fields = '__all__'
    def get_product(self, obj):
        return obj.product.name
