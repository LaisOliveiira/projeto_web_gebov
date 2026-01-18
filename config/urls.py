from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Inclui as rotas do seu app de autenticação
    path('', include('autenticacao.urls')),
    
    # Aqui você incluirá o app de eventos no futuro
    # path('eventos/', include('eventos.urls')),
]