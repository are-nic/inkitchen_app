from django.db import models
from django.shortcuts import reverse
from food.models import TagProduct
from django.contrib.auth import get_user_model

User = get_user_model()


class CategoryProduct(models.Model):
    """
    Категории товаров
    """
    name = models.CharField(max_length=200, verbose_name="Название категории")
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'CategoryProduct'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('market:product_list_by_category', args=[self.slug])


class ProductMarket(models.Model):
    category = models.ForeignKey(CategoryProduct, related_name='products', verbose_name='Категория', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    name = models.CharField(max_length=300, verbose_name='Наименование')
    # qty_per_item = models.PositiveIntegerField(verbose_name='Кол-во на ед. продукта')
    # unit = models.CharField(max_length=10, verbose_name='Ед. измерения')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Описание')        # delete
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Остаток')
    tags = models.ManyToManyField(TagProduct, blank=True, verbose_name='Тэги', related_name='products')
    available = models.BooleanField(default=True, verbose_name='В наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')    # delete
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')      # delete

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'ProductMarket'

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class OrderMarket(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Покупатель')
    date_order = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    complete = models.BooleanField(default=False, null=True, blank=False, verbose_name='Выполнен')
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property       # дает возожность обращаться к методу в шаблоне
    def get_total_cart(self):
        """
        стоимость всего заказа
        """
        order_items = self.orderitemmarket_set.all()
        total = sum([item.get_total_item for item in order_items])
        return total


class OrderItemMarket(models.Model):
    product = models.ForeignKey(ProductMarket, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(OrderMarket, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Кол-во')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Товар добавлен')

    @property
    def get_total_item(self):
        """
        определить стоимость продукта в заказе
        """
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Покупатель')
    order = models.ForeignKey(OrderMarket, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Заказ')
    address = models.CharField(max_length=200, null=True, verbose_name='Адрес')
    city = models.CharField(max_length=200, null=True, verbose_name='Город')
    region = models.CharField(max_length=200, null=True, verbose_name='Регион')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.address
