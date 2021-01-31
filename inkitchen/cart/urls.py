from django.urls import path
from .views import cart_detail, cart_add, adjust_cart, remove_recipe_from_cart

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<id>', cart_add, name='cart_add'),
    path('adjust/<id>', adjust_cart, name='adjust_cart'),
    path('remove/<id>', remove_recipe_from_cart, name='remove_from_cart'),
]