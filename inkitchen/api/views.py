from food.models import Recipe
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status, permissions
from .serializers import RecipeListSerializer, RecipeDetailSerializer


class RecipeListView(APIView):
    """вывод списка рецептов"""
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        recipes = Recipe.objects.all()                          # получаем все рецепты из БД (queryset)
        serializer = RecipeListSerializer(recipes, many=True)   # передаем в сериалайзер queryset рецептов
        return Response(serializer.data)                        # возвращаем данные сериализатора в JSON'e

    def post(self, request):
        recipe = request.data
        # создать рецепт из приведенных выше данных
        serializer = RecipeDetailSerializer(data=recipe)
        if serializer.is_valid(raise_exception=True):
            recipe_saved = serializer.save()
            return Response({"success": "Рецепт '{}' успешно создан".format(recipe_saved.title)})


class RecipeDetailView(APIView):
    """вывод одного рецепта"""
    def get(self, request, pk):
        recipe = Recipe.objects.get(id=pk)                      # получаем рецепт из БД по id
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, pk):
        recipe = Recipe.objects.get(id=pk)
        serializer = RecipeDetailSerializer(recipe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recipe = Recipe.objects.get(id=pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)