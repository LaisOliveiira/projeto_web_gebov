from django.db import models
from autenticacao.models import Usuario # Importando seu modelo personalizado

class TipoEvento(models.Model):
    """Define se é Mini Curso ou Palestra."""
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'tipo_evento'

    def __str__(self):
        return self.nome

class Evento(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    
    # Novos campos solicitados
    data_evento = models.DateField(verbose_name="Data do Evento")
    horario_evento = models.TimeField(verbose_name="Horário do Evento")
    responsavel = models.CharField(max_length=255, verbose_name="Palestrante/Responsável")
    
    local = models.CharField(max_length=255, verbose_name="Local")
    
    # Chaves Estrangeiras seguindo o padrão RESTRICT do Lumon
    tipo = models.ForeignKey(
        TipoEvento, 
        on_delete=models.RESTRICT, 
        verbose_name="Tipo de Evento"
    )
    cadastrado_por = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        verbose_name="Usuário que Cadastrou"
    )
    
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'evento'
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return f"{self.titulo} - {self.responsavel}"

class Inscricao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Participante")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name="Evento")
    data_inscricao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inscricao'
        # Garante que o usuário não se inscreva duas vezes no mesmo evento
        unique_together = ('usuario', 'evento') 

    def __str__(self):
        return f"{self.usuario.nome} em {self.evento.titulo}"
