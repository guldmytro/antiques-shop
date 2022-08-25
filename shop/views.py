from django.shortcuts import render, get_object_or_404
from .models import Product


def catalog(request, slug=None):
    return render(request, 'product/list.html', {})


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug)
    return render(request, 'product/detail.html', {'product': product})
