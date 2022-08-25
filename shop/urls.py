from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('product-tag/<slug:slug>/', views.catalog, name='by_tag'),
    path('<int:pk>/<slug:slug>/', views.product_detail, name='product_detail'),
]