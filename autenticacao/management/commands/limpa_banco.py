from django.core.management.base import BaseCommand
from autenticacao.models import Perfil, Usuario

class Command(BaseCommand):
    help = 'Limpa todos os dados de usuários e perfis do banco de dados'

    def add_arguments(self, parser):
        # Adiciona um argumento para confirmar a exclusão e evitar acidentes
        parser.add_argument(
            '--force',
            action='store_true',
            help='Executa a limpeza sem pedir confirmação',
        )

    def handle(self, *args, **kwargs):
        if not kwargs['force']:
            confirmacao = input("Isso apagará TODOS os usuários e perfis. Tem certeza? (s/n): ")
            if confirmacao.lower() != 's':
                self.stdout.write(self.style.WARNING("Operação cancelada."))
                return

        self.stdout.write("Limpando banco de dados...")

        # A ordem aqui importa devido às chaves estrangeiras (ForeignKeys)
        # Primeiro deletamos os usuários, depois os perfis
        total_usuarios = Usuario.objects.all().count()
        Usuario.objects.all().delete()
        self.stdout.write(f"✓ {total_usuarios} usuários removidos.")

        total_perfis = Perfil.objects.all().count()
        Perfil.objects.all().delete()
        self.stdout.write(f"✓ {total_perfis} perfis removidos.")

        self.stdout.write(self.style.SUCCESS("Banco de dados limpo com sucesso!"))