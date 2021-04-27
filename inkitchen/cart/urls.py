from django.urls import path
from .views import cart_add, adjust_cart, remove_recipe_from_cart, add_to_cart

urlpatterns = [
    path('add/<id>', cart_add, name='cart_add'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('adjust/<id>', adjust_cart, name='adjust_cart'),
    path('remove/<id>', remove_recipe_from_cart, name='remove_from_cart'),
]