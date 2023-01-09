from django.urls import path
from . import views

urlpatterns = [
    path('giris/', views.login, name='giris'),
    path('kayit/', views.register, name='kayit'),
    path('cikis/', views.logout, name='cikis'),
    ]