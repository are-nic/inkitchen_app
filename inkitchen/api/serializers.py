from rest_framework import serializers
from django.contrib.auth import get_user_model
from food.models import Recipe

User = get_user_model()


class RecipeListSerializer(serializers.ModelSerializer):
    """Список рецептов"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ('id', 'owner', 'category', 'title', 'image')

    def create(self, validated_data):
        return Recipe.objects.create(**validated_data)


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Один рецепт"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    ingredients = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = ('owner',
                  'category',
                  'title',
                  'slug',
                  'image',
                  'price',
                  'description',
                  'cooking_time',
                  'group',
                  'date_created',
                  'tags')

    def update(self, instance, validated_data):
        """
        Обновить и вернуть существующий экземпляр Рецепта
        """
        instance.category = validated_data.get('category', instance.category)
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.image = validated_data.get('image', instance.image)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.ingredients = validated_data.get('ingredients', instance.ingredients)
        instance.save()
        return instance
