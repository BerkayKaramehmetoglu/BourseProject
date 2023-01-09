from django.urls import path
from .consumers import MoneyConsumer
ws_urlpatterns = [
    path_as('ws/money/', MoneyConsumer.asgi()),
]