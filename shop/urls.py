from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]