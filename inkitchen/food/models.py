from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Shop(models.Model):       # магазин продуктов (Азбука Вкуса, Пешеход и тд)

    name = models.CharField(max_length=100, verbose_name="Название магазина")
    logo = models.ImageField(verbose_name='Логотип магазина', blank=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        db_table = 'Shop'

    def __str__(self):
        return self.name


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


class TagIngredient(models.Model):
    """
    Тэги для ингредиентов
    """
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Тэг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг ингредиентов'
        verbose_name_plural = 'Тэги ингредиентов'
        db_table = 'tags_ingredients'

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
    OFFICE = 'OFFICE'
    HOME = 'HOME'
    GROUP_RECIPE = [
        (OFFICE, 'Для офиса'),
        (HOME, 'Для дома'),
    ]

    owner = models.ForeignKey(User, verbose_name='Автор рецепта', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название рецепта')
    slug = models.SlugField(unique=True)
    cooking_time = models.CharField(max_length=50, verbose_name='Время приготовления')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Фото блюда', blank=True, null=True, upload_to='recipes')
    group = models.CharField(max_length=6, choices=GROUP_RECIPE, default=HOME, verbose_name='Группа рецепта')
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


class IngredientOfRecipe(models.Model):
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
    name = models.ForeignKey(TagIngredient, verbose_name='Тэг', on_delete=models.CASCADE, related_name='ingredient_name')
    qty = models.PositiveIntegerField(verbose_name='Кол-во')
    unit = models.CharField(max_length=20, choices=UNITS, verbose_name='Ед. измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        db_table = 'Ingredient_Of_Recipe'

    def __str__(self):
        return self.name.name


class Product(models.Model):
    """
    Экземпляр продукта, который поставляется магазинами. Каждый ингредиент может ссылаться на несколько продуктов
    одного вида
    """
    # поля, получаемые от магазинов
    shop = models.ForeignKey(Shop, verbose_name='Магазин', on_delete=models.CASCADE)
    name = models.CharField(max_length=300, verbose_name='Наименование продукта')
    qty_per_item = models.PositiveIntegerField(verbose_name='Кол-во на ед. продукта')
    stock = models.PositiveIntegerField(verbose_name='Остаток')            # остаток единиц продукта в магазине
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    unit = models.CharField(max_length=10, verbose_name='Ед. измерения')
    tag = models.ForeignKey(TagIngredient, verbose_name='Тэг ингредиента',
                            on_delete=models.CASCADE, related_name='product')
    # Доп. поля
    protein = models.CharField(max_length=10, verbose_name='Белки', blank=True)
    fats = models.CharField(max_length=10, verbose_name='Жиры', blank=True)
    carbohydrate = models.CharField(max_length=10, verbose_name='Углеводы', blank=True)
    kkal = models.CharField(max_length=30, verbose_name='Ккал', blank=True)
    available = models.BooleanField(default=True, verbose_name='В наличии')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'Product'

    def __str__(self):
        return self.name