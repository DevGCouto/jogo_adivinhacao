from django.urls import path
from .views import jogo_adivinhacao

urlpatterns = [
    path('', jogo_adivinhacao, name='jogo'),
]
