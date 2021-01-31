from django.urls import path
from . import views
from users.views import continue_register


urlpatterns = [
    path('', continue_register, name='home'),
    path('about', views.about, name='about'),
]
