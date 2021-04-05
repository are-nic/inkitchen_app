from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """
    категории рецептов
    """
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'CategoryRecipe'

    def __str__(self):
        return self.name


class TagProduct(models.Model):
    """
    Тэги продуктов
    """
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Тэг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг продуктов'
        verbose_name_plural = 'Тэги продуктов'
        db_table = 'tags_products'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    """
    Тэги для рецептов
    """
    name = models.CharField(max_length=100, verbose_name='Тэг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг рецептов'
        verbose_name_plural = 'Тэги рецептов'
        db_table = 'tags_recipes'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Рецепт
    """

    owner = models.ForeignKey(User, verbose_name='Автор рецепта', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название рецепта')
    slug = models.SlugField(unique=True)
    cooking_time = models.CharField(max_length=50, verbose_name='Время приготовления')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Фото блюда', blank=True, null=True, upload_to='recipes')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена',
                                default=0.01, validators=[MinValueValidator(Decimal('0.01'))])
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='создан')
    tags = models.ManyToManyField(TagRecipe, blank=True, default='рецепт', verbose_name='Тэги')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        db_table = 'Recipe'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        для автоматического заполнения поля slug при создании рецепта
        """
        self.slug = slugify(self.title)
        return super(Recipe, self).save(*args, **kwargs)


class Ingredient(models.Model):
    """
    экземпляр ингридиента, который принадлежит к конкретному рецепту в определенном кол-ве.
    для получения всех ингридиентов по какому либо рецепту использовать: recipe.ingredients.all()
    """

    UNITS = [
        ('LITER', 'л.'),
        ('MILLI', 'мл.'),
        ('GRAMM', 'г.'),
        ('KILO', 'кг.'),
        ('PIECES', 'шт.'),
        ('TASTE', 'по вкусу'),
        ('TEA SPOON', 'ч. ложка'),
        ('TABLESPOON', 'ст. ложка'),
        ('GLASS', 'стакан'),
    ]

    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE, related_name='ingredients')
    name = models.ForeignKey(TagProduct, verbose_name='Тэг', on_delete=models.CASCADE, related_name='ingredient_name')
    qty = models.PositiveIntegerField(verbose_name='Кол-во')
    unit = models.CharField(max_length=20, choices=UNITS, verbose_name='Ед. измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        db_table = 'Ingredient'

    def __str__(self):
        return self.name.name