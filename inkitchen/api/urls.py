from django.urls import path, include
from .views import RecipeListView, RecipeDetailView


urlpatterns = [
    path('recipes', RecipeListView.as_view()),
    path('recipes/<int:pk>/', RecipeDetailView.as_view()),
    path('auth/', include('rest_framework.urls')),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls.jwt')),
]