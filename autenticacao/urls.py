from django.urls import path
from . import views
from eventos.views import *

urlpatterns = [
    # Tela de Login (Raiz do app auth)
    path('', views.login_view, name='login'),
    # Tela Principal pós-login
    path('home/', views.home_view, name='home'),
    # Rota para encerrar a sessão
    path('logout/', views.logout_view, name='logout'),
    path('alterar-senha/', views.alterar_senha_view,
         name='alterar_senha'),  # <-- Nova rota
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
]
