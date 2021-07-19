from django.urls import path
from .views import adjust_cart, remove_from_cart, add_to_cart

urlpatterns = [
    path('add_to_cart/', add_to_cart, name='add_to_cart'),  # исправить путь после удаление верхнего роута на cart_add
    path('adjust/', adjust_cart, name='adjust_cart'),
    path('remove/', remove_from_cart, name='remove_from_cart'),
]

'''
просмотреть содержимое сессии

python manage.py shell

from django.contrib.sessions.models import Session
Session.objects.all()
Session.objects.get(pk='7o5hrpck8nndmg0r8w71go82xiv63qpb').get_decoded()
'''