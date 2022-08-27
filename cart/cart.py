from decimal import Decimal
from urllib import request
from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        if override_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        else:
            self.cart[product_id]['quantity'] += int(quantity)
        self.save()
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            if 'product' in item:
                item['total_price'] = Decimal(item['product'].price) * item['quantity']
                item['total_price_regular'] = Decimal(item['product'].price_regular) * item['quantity']
                yield item
    
    def get_total_price(self):
        total_price = 0
        for item in self.cart.values():
            if 'product' in item:
                total_price += Decimal(item['product'].price) * item['quantity']
        return total_price
    
    def get_cart_cnt(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products.count()
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def save(self):
        self.session.modified = True
        
