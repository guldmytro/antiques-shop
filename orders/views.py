from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem, Order
from cart.cart import Cart
from orders.forms import OrderCreateForm
from django.urls import reverse
from .tasks import order_created, order_notification
import braintree
from django.conf import settings
from .utils import test_order_created


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
    if cart.get_cart_cnt() == 0:
        return redirect('cart:list')

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
            test_order_created(order.id)
            order_created.delay(order.id)
            order_notification.delay(order.id)
            return render(request, 'orders/order/created.html',
            {'order': order, 'breadcrumbs': breadcrumbs})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html',
    {'cart': cart, 'form': form, 'breadcrumbs': breadcrumbs})


gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def order_pay(request, id, uuid):
    order = get_object_or_404(Order, id=id, secret_id=uuid, paid=False)
    total_cost = order.get_total_cost()
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        # создание и отправка транзакции
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('orders:order_pay_done', id=order.id, uuid=order.secret_id)
        else:
            return redirect('orders:order_pay_canceled', id=order.id, uuid=order.secret_id)
    else:
        # Генерация токена
        client_token = gateway.client_token.generate()
        return render(request, 'orders/order/pay.html', 
        {'order': order, 'client_token': client_token})

def payment_done(request, id, uuid):
    order = get_object_or_404(Order, id=id, secret_id=uuid, paid=True)
    return render(request, 'orders/order/paymnent_done.html')

def payment_canceled(request, id, uuid):
    order = get_object_or_404(Order, id=id, secret_id=uuid, paid=False)
    return render(request, 'orders/order/paymnent_canceled.html')
    
