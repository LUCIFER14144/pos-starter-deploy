from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=200)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.name} ({self.sku})"

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    qty = models.IntegerField(default=0)

class Sale(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    cashier = models.CharField(max_length=100, null=True, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

class Negotiation(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='negotiations')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)
    proposer = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    changed_by = models.CharField(max_length=100, blank=True)
    reason = models.CharField(max_length=200, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
