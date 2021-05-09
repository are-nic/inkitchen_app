from django.urls import path
from .views import all_recipes, create_recipe, RecipeDetailView, edit_recipe, remove_recipe, delivery_day


urlpatterns = [
    path('', all_recipes, name='recipes'),
    path('week/<slug:index>', delivery_day, name='delivery_day'),
    path('create', create_recipe, name='create_recipe'),
    path('edit/<id>', edit_recipe, name='edit_recipe'),
    path('remove/<id>', remove_recipe, name='remove_recipe'),
    path('<slug:slug>', RecipeDetailView.as_view(), name='recipe_details'),
]