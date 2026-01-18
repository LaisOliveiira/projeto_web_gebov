from django.urls import path
from . import views

urlpatterns = [
    # Rota: localhost:8000/eventos/cadastro/
    path('cadastro/', views.cadastro_evento_view, name='cadastro_evento'),
]