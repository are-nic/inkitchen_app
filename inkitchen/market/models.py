from django.db import models
from django.shortcuts import reverse
from food.models import TagIngredient


class CategoryProduct(models.Model):
    """
    Категории товаров
    """
    name = models.CharField(max_length=200, verbose_name="Название категории")
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'
        db_table = 'CategoryProduct'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('market:product_list_by_category', args=[self.slug])


class ProductMarket(models.Model):
    category = models.ForeignKey(CategoryProduct, related_name='products', verbose_name='Категория', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    name = models.CharField(max_length=300, verbose_name='Наименование')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Остаток')
    tags = models.ManyToManyField(TagIngredient, blank=True, verbose_name='Тэги', related_name='products')
    available = models.BooleanField(default=True, verbose_name='В наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт магазина'
        verbose_name_plural = 'Продукты магазина'
        db_table = 'ProductMarket'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('market:product_detail', args=[self.id])