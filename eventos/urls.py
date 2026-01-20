from django.urls import path
from . import views
from autenticacao.views import *

urlpatterns = [
    # Rota: localhost:8000/eventos/cadastro/
    path('cadastro/', views.cadastro_evento_view, name='cadastro_evento'),
    path('gerenciar/', views.gerenciar_eventos_view, name='gerenciar_eventos'),
    path('inscrever/', views.inscrever_evento_view, name='inscrever_evento'),
]