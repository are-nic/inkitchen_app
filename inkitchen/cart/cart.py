'''from decimal import Decimal
from django.conf import settings
from food.models import Recipe


class Cart:

    def __init__(self, request):
        """
        Инициализируем корзину
        Мы ожидаем, что наш словарь корзины будет использовать id рецептов в качестве ключей и словарь с количеством
        и ценой в качестве значения для каждого ключа. Таким образом, мы можем гарантировать, что продукт не будет
        добавлен в корзину более одного раза
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)       # получить корзину из текущей сессии
        if not cart:                                            # если в сессии отсутствует корзина
            # сохраняем пустую корзину в сессии в виде пустого словаря
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, recipe, quantity=1, update_quantity=False):
        """
        Добавить рецепт в корзину или обновить его количество.
        recipe : Экземпляр рецепта для добавления или обновления в корзине
        quantity : Необязательное целое число для количества продукта. По умолчанию используется значение 1 .
        update_quantity : Это логическое значение, которое указывает, требуется ли обновление количества с заданным
        количеством (True), или же новое количество должно быть добавлено к существующему количеству (False).

        id рецепта используется в качестве ключа в словаре содержимого корзины. id рецепта преобразуется в строку,
        так как Джанго использует JSON для сериализации данных сессии, а JSON разрешает только имена строк.
        id рецепта — это ключ, а значение, которое мы сохраняем, — словарь с количеством (quantity) и ценой (price)
        для рецепта. Цена рецепта преобразуется из десятичного разделителя в строку, чтобы сериализовать ее.
        """
        recipe_id = str(recipe.id)
        if recipe_id not in self.cart:
            self.cart[recipe_id] = {'quantity': 0, 'price': str(recipe.price)}
        if update_quantity:
            self.cart[recipe_id]['quantity'] = quantity
        else:
            self.cart[recipe_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        сохраняет все изменения корзины в сессии и помечает сессию как modified с помощью session.modified = True.
        Это говорит о том, что сессия modified и должна быть сохранена.
        """
        # Обновление сессии корзины
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, recipe):
        """
        Удаление товара из корзины
        удаляет заданный продукт из словаря корзины и вызывает метод save() для обновления корзины в сессии.
        """
        recipe_id = str(recipe.id)
        if recipe_id in self.cart:
            del self.cart[recipe_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        recipe_ids = self.cart.keys()
        # получение объектов recipes и добавление их в корзину
        recipes = Recipe.objects.filter(id__in=recipe_ids)
        for recipe in recipes:
            self.cart[str(recipe.id)]['recipe'] = recipe

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """удаление корзины из сессии"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True'''