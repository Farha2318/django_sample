from django.urls import path
from . import views

urlpatterns = [
    path('', views.crypto_view, name='crypto_home'),
]
