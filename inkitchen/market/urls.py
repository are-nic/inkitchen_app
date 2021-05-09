from django.urls import path
from .views import product_list, update_item


urlpatterns = [
    path('', product_list, name='product_list'),
    path('<slug:category_slug>', product_list, name='product_list_by_category'),
    path('update_item/', update_item, name='update_item'),
]