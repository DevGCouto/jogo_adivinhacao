from django.contrib import admin
from django.urls import path
from meu_app.views import jogo_adivinhacao, forcar_migracao  

urlpatterns = [
    path('', jogo_adivinhacao),
    path('admin/', admin.site.urls),
    path('forcar-migracao/', forcar_migracao),
]
