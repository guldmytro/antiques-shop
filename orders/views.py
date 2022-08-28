from django.shortcuts import render
from .models import OrderItem
from cart.cart import Cart
from orders.forms import OrderCreateForm
from django.urls import reverse


def order_create(request):
    breadcrumbs = [
        {
            'label': 'Каталог товаров',
            'url': reverse('shop:catalog'),
            'type': 'link'
        },
        {
            'label': 'Корзина',
            'url': reverse('cart:list'),
            'type': 'link'
        },
        {
            'label': 'Оформление заказа',
            'type': 'text'
        },
    ]
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                if 'product' in item:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['product'].price,
                        quantity=item['quantity']
                    )
            cart.clear()
            return render(request, 'orders/order/created.html',
            {'order': order, 'breadcrumbs': breadcrumbs})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html',
    {'cart': cart, 'form': form, 'breadcrumbs': breadcrumbs})
