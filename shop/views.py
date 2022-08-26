from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from .utils import get_filters, filter_query, get_page_link_strings, order_query, filter_by_search_form
from django.urls import reverse
from .forms import SearchForm


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
    
    query_string = None
    if request.GET.get('query'):
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            cd = search_form.cleaned_data
            query_string = cd['query']
            object_list = filter_by_search_form(object_list, query_string)
            title = f'Результаты поиска: <em>"{query_string}"</em>'
    if not request.is_ajax():
        filters = get_filters(tag, query_string)

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
