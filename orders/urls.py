from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('pay/<int:id>/<uuid:uuid>/', views.order_pay, name='order_pay'),
    path('done/<int:id>/<uuid:uuid>/', views.payment_done, name='order_pay_done'),
    path('canceled/<int:id>/<uuid:uuid>/', views.payment_canceled, name='order_pay_canceled'),
]