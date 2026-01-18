from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Perfil(models.Model):
    """Define se é Admin, Gerente ou Cliente."""
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    """Modelo personalizado baseado no Sistema Lumon."""
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    perfil = models.ForeignKey(Perfil, on_delete=models.RESTRICT)
    # Exemplo de campo extra para o futuro
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Hasheia a senha automaticamente como no Lumon
        if self.senha and not self.senha.startswith('pbkdf2_sha256$'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def verificar_senha(self, senha_texto):
        return check_password(senha_texto, self.senha)