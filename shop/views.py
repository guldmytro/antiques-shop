from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from .utils import get_filters


def catalog(request, slug=None):
    object_list = Product.objects.all()
    tag = None
    filters = None
    template = 'product/list.html'
    if slug:
        tag = get_object_or_404(Tag, slug=slug)
        object_list = object_list.filter(tags__in=[tag])
    if not request.is_ajax():
        filters = get_filters(tag)
    else:
        template = 'product/list_tag.html'

    count = object_list.count()
    paginator = Paginator(object_list, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request,
                  template,
                  {'page': page,
                   'products': products,
                   'count': count,
                   'filters': filters})


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug)
    return render(request, 'product/detail.html',
                  {'product': product})
