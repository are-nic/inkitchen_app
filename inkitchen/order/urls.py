from django.urls import path
from .views import order_create, get_current_location, order_created

urlpatterns = [
    path('create', order_create, name='order_create'),
    path('created', order_created, name='order_created'),
    path('get_current_location', get_current_location, name='get_current_location'),
]