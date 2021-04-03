from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('recipes/', include('food.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('api/v1/', include('api.urls')),
    path('market/', include(('market.urls', 'app_name'), namespace='market')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:      # если проект в режиме Дебаг, то директории для медиафайлов здесь
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)