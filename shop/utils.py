from attribute.models import *
from django.db.models import Q


def get_filters(tag, query):
    attributes = [
        {
            'name': 'holiday',
            'title': 'По праздникам',
            'obj': Holiday,
            'queryset': None
        },
        {
            'name': 'age',
            'title': 'Подарки по году рождения',
            'obj': Age,
            'queryset': None
        },
        {
            'name': 'event',
            'title': 'Подарки на памятные события',
            'obj': Event,
            'queryset': None
        },
        {
            'name': 'travel',
            'title': 'Подарки путешественникам',
            'obj': Travel,
            'queryset': None
        },
        {
            'name': 'subject',
            'title': 'Подарки по темам',
            'obj': Subject,
            'queryset': None
        },
        {
            'name': 'profession',
            'title': 'Подарки по профессиям',
            'obj': Profession,
            'queryset': None
        },
    ]
    for attribute in attributes:
        if tag:
            attribute_values = attribute['obj'].objects.filter(products__tags__in=[tag])
        elif query:
            attribute_values = attribute['obj'].objects.filter(products__name__icontains=query)
        else:
            attribute_values = attribute['obj'].objects.filter(products__price__gt=0)
        attribute['queryset'] = attribute_values.order_by('name').distinct()
        attribute.pop('obj')
    return attributes


def filter_query(queryset, query_dict):
    FILTERS = [
        'holiday',
        'age',
        'event',
        'travel',
        'subject',
        'profession'
    ]
    for key, values in query_dict:
        # Если выборка пустая, фильтровать нету смысла
        if queryset.count() == 0:
            return queryset
        q = Q()

        # Фильтрация по цене
        if key == 'price':
            for val in values:
                prices = parse_prices(val)
                if prices:
                    q |= Q(price__gte=prices['min'], price__lt=prices['max'])

        # Если ключ не сортировка и не сортировка, значит атрибут
        elif key in FILTERS:
            for val in values:
                query_key = f'{key}__slug'
                q |= Q(**{query_key: val})
        queryset = queryset.filter(q)
    return queryset


def filter_by_search_form(queryset, query):
    queryset = queryset.filter(name__icontains=query)
    return queryset


def parse_prices(prices):
    price_list = [int(i) for i in prices.split('-')]
    if len(price_list) < 2:
        return False

    return {
        'min': min(price_list),
        'max': max(price_list)
    }

def order_query(queryset, request):
    ordering = request.GET.get('order')
    if ordering:
        if ordering == 'date-desc':
            queryset = queryset.order_by('-created')
        elif ordering == 'date-asc':
            queryset = queryset.order_by('created')
        elif ordering == 'price-asc':
            queryset = queryset.order_by('price')
        elif ordering == 'price-desc':
            queryset = queryset.order_by('-price')
    return queryset


def get_page_link_strings(request):
    pagination_link_startwith = '?'
    sep = ''
    full_path = request.get_full_path()

    if '&page=' in full_path:
        sep = '&page='
    else:
        sep = '?page='

    page_link_prefix = full_path.split(sep)[0]

    
    if '?page=' in full_path:
        pagination_link_startwith = '?'
    elif '?' in full_path:
        pagination_link_startwith = '&'

    return (pagination_link_startwith, page_link_prefix)
