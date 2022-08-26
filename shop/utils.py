from attribute.models import *


def get_filters(tag):
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
        else:
            attribute_values = attribute['obj'].objects.filter(products__price__gt=0)
        attribute['queryset'] = attribute_values.distinct()
        attribute.pop('obj')
    return attributes
