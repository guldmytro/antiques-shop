from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from shop.models import Product
from .forms import CartAddProductForm
from django.urls import reverse


def cart_list(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    breadcrumbs = [
        {
            'label': 'Каталог товаров',
            'url': reverse('shop:catalog'),
            'type': 'link'
        },
        {
            'label': 'Корзина',
            'type': 'text'
        },

    ]
    return render(request, 'cart/list.html', {
        'cart': cart,
        'breadcrumbs': breadcrumbs,
    })


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, 
        quantity=cd['quantity'], 
        override_quantity=cd['override'])
    return redirect('cart:list')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:list')