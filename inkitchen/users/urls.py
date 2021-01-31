from django.urls import path, include
from . import urls_reset, urls_change
from .views import register, profile, logout, login, profile_view, upgrade_profile, remove_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),                                  # отображение страницы текущего юзера
    path('upgrade/<int:user_id>', upgrade_profile, name='upgrade_profile'),     # изменение информации текущего юзера
    path('remove/<int:user_id>', remove_profile, name='remove_profile'),        # удаление текущего юзера
    path('profile/<int:user_id>', profile_view, name='profile_view'),           # отображение сраницы юзеров по id
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('password-reset/', include(urls_reset)),
    path('password-change/', include(urls_change)),
]
