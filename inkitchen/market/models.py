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
    category = models.ForeignKey(CategoryProduct, related_name='products', verbose_name='Категория',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=300, verbose_name='Наименование')
    # qty_per_item = models.PositiveIntegerField(verbose_name='Кол-во на ед. продукта')
    # unit = models.CharField(max_length=10, verbose_name='Ед. измерения')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Описание')        # delete
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Остаток')
    tags = models.ManyToManyField(TagProduct, blank=True, verbose_name='Тэги', related_name='products')
    available = models.BooleanField(default=True, verbose_name='В наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

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

    class Meta:
        ordering = ('date_order',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'Order_Market'

    def __str__(self):
        return str(self.id)

    @property       # дает возожность обращаться к методу в шаблоне для вывода цен
    def get_cart_total(self):
        """
        стоимость всего заказа
        """
        order_items = self.orderitemmarket_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        """
        кол-во продуктов в корзине
        """
        order_items = self.orderitemmarket_set.all()
        total = sum([item.quantity for item in order_items])
        return total


class OrderItemMarket(models.Model):
    product = models.ForeignKey(ProductMarket, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(OrderMarket, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Кол-во')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Товар добавлен')

    class Meta:
        ordering = ('date_added',)
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'
        db_table = 'Order_Item_Market'

    @property
    def get_total(self):
        """
        определить стоимость продукта в заказе в зависимости от количества
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

    class Meta:
        ordering = ('order',)
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'
        db_table = 'Shipping_Address'

    def __str__(self):
        return self.address
