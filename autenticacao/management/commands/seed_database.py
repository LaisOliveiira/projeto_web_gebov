from django.core.management.base import BaseCommand
from autenticacao.models import Perfil, Usuario

class Command(BaseCommand):
    help = 'Popula o banco com perfis e usuários iniciais'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando população do banco...")

        # 1. Criar Perfis
        nomes_perfis = ['Admin', 'Empresa', 'Cliente']
        perfis_criados = {}
        for nome in nomes_perfis:
            perfil, _ = Perfil.objects.get_or_create(nome=nome)
            perfis_criados[nome] = perfil
            self.stdout.write(f"✓ Perfil '{nome}' pronto.")

        # 2. Criar Usuários de Teste (Senhas serão hasheadas pelo save do Model)
        usuarios_teste = [
            {'nome': 'Admin Teste', 'email': 'admin@teste.com', 'perfil': 'Admin'},
            {'nome': 'Empresa Teste', 'email': 'empresa@teste.com', 'perfil': 'Empresa'},
            {'nome': 'Cliente Teste', 'email': 'cliente@teste.com', 'perfil': 'Cliente'},
        ]

        for dados in usuarios_teste:
            if not Usuario.objects.filter(email=dados['email']).exists():
                Usuario.objects.create(
                    nome=dados['nome'],
                    email=dados['email'],
                    senha='123',  # Será criptografada automaticamente
                    perfil=perfis_criados[dados['perfil']]
                )
                self.stdout.write(f"✓ Usuário '{dados['nome']}' criado (Senha: 123).")

        self.stdout.write(self.style.SUCCESS("Banco de dados pronto para uso!"))