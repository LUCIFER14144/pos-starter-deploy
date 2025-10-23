from decimal import Decimal
from django.db import transaction
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Inventory, Sale, SaleItem, Negotiation, PriceHistory
from .serializers import ProductSerializer, SaleSerializer, NegotiationSerializer

AUTO_APPROVE_DISCOUNT_PERCENT = Decimal('10')

@api_view(['GET'])
def products_list(request):
    qs = Product.objects.all()
    return Response(ProductSerializer(qs, many=True).data)

@api_view(['POST'])
def create_product(request):
    data = request.data
    p = Product.objects.create(sku=data.get('sku'), name=data.get('name'), cost_price=data.get('cost_price',0), list_price=data.get('list_price'))
    Inventory.objects.create(product=p, qty=data.get('qty',0))
    return Response({'id': p.id})

@api_view(['POST'])
def create_sale(request):
    # payload: { cashier: '', items: [ { product_id, qty, proposed_unit_price, proposer } ] }
    payload = request.data
    items = payload.get('items', [])
    if not items:
        return Response({'error':'no items'}, status=400)
    with transaction.atomic():
        sale = Sale.objects.create(cashier=payload.get('cashier',''))
        total = Decimal('0')
        for it in items:
            prod = Product.objects.select_for_update().get(id=it['product_id'])
            inv, _ = Inventory.objects.get_or_create(product=prod)
            qty = int(it.get('qty',1))
            list_price = prod.list_price
            final_unit = list_price
            if 'proposed_unit_price' in it and it['proposed_unit_price'] is not None:
                proposed = Decimal(str(it['proposed_unit_price']))
                discount_pct = (1 - (proposed / list_price)) * 100
                if discount_pct <= AUTO_APPROVE_DISCOUNT_PERCENT:
                    final_unit = proposed
                    PriceHistory.objects.create(product=prod, old_price=list_price, new_price=proposed, changed_by=it.get('proposer','clerk'), reason='negotiated unit price (auto)')
                else:
                    Negotiation.objects.create(sale=sale, product=prod, proposed_price=proposed, proposer=it.get('proposer',''))
                    final_unit = proposed
            line_total = final_unit * qty
            SaleItem.objects.create(sale=sale, product=prod, qty=qty, unit_price=final_unit, line_total=line_total)
            inv.qty -= qty
            inv.save()
            total += line_total
        sale.total = total
        sale.save()
        return Response({'sale_id': sale.id, 'total': str(total)})

@api_view(['GET'])
def negotiations_list(request):
    qs = Negotiation.objects.select_related('product').order_by('-created_at')
    return Response(NegotiationSerializer(qs, many=True).data)

@api_view(['POST'])
def approve_negotiation(request, nid):
    # expects { approver: 'manager', pin: '1234' }
    try:
        neg = Negotiation.objects.select_for_update().get(id=nid)
    except Negotiation.DoesNotExist:
        return Response({'error':'not found'}, status=404)
    pin = request.data.get('pin')
    if not pin or pin != getattr(settings, 'MANAGER_PIN', None):
        return Response({'error':'invalid manager PIN'}, status=403)
    with transaction.atomic():
        neg.status = 'approved'
        neg.save()
        # update related sale_item(s)
        items = SaleItem.objects.filter(sale=neg.sale, product=neg.product)
        for si in items:
            si.unit_price = neg.proposed_price
            si.line_total = si.unit_price * si.qty
            si.save()
        # recompute sale total
        total = sum([si.line_total for si in SaleItem.objects.filter(sale=neg.sale)])
        neg.sale.total = total
        neg.sale.save()
        PriceHistory.objects.create(product=neg.product, old_price=None, new_price=neg.proposed_price, changed_by=request.data.get('approver','manager'), reason=f'negotiation approved id:{neg.id}')
        return Response({'ok':True})

@api_view(['POST'])
def verify_manager_pin(request):
    pin = request.data.get('pin')
    if pin and pin == getattr(settings, 'MANAGER_PIN', None):
        return Response({'ok': True})
    return Response({'ok': False}, status=403)
