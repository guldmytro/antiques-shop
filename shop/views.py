from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from .utils import get_filters, filter_query, get_page_link_strings, order_query
from django.urls import reverse


def catalog(request, slug=None):
    object_list = Product.objects.all()
    tag = None
    filters = None
    template = 'product/list.html'
    query_filters = request.GET.lists()
    title = None
    
    if slug:
        tag = get_object_or_404(Tag, slug=slug)
        title = tag.name.capitalize()
        object_list = object_list.filter(tags__in=[tag])
    if not request.is_ajax():
        filters = get_filters(tag)

    if '?' in request.get_full_path():
        object_list = filter_query(object_list, query_filters)

    pagination_link_startwith, page_link_prefix = get_page_link_strings(request)
    object_list = order_query(object_list, request)
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
                   'title': title,
                   'page_link_prefix': page_link_prefix,
                   'pagination_link_startwith': pagination_link_startwith,
                   'section': 'catalog',
                   'products': products,
                   'count': count,
                   'filters': filters})


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, id=pk, slug=slug)
    breadcrumbs = [
        {
            'label': 'Каталог товаров',
            'url': reverse('shop:catalog'),
            'type': 'link'
        }
    ]
    if product.tags.count():
        tag = product.tags.first()
        print(tag.slug)
        breadcrumbs.append({
            'label': tag.name,
            'url': reverse('shop:by_tag', args=[tag.slug]),
            'type': 'link'
        })
    breadcrumbs.append({
        'label': product.name,
        'type': 'text'
    })
    return render(request, 'product/detail.html',
                  {'product': product,
                   'breadcrumbs': breadcrumbs,
                   'section': 'product'})
