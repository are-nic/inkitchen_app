from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from django.urls import path

urlpatterns = [
    path('', PasswordChangeView.as_view(), name='password_change'),
    path('done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
]