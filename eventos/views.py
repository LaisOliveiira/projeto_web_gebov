from django.shortcuts import render, redirect
from .models import Evento, TipoEvento
from autenticacao.models import Usuario
from django.contrib import messages


def cadastro_evento_view(request):
    # Proteção de acesso (Padrão Lumon)
    if 'user_id' not in request.session:
        messages.warning(request, 'Você precisa fazer login primeiro.')
        return redirect('login')

    if request.session.get('user_perfil') not in ['Empresa', 'Admin']:
        messages.error(request, 'Acesso negado.')
        return redirect('home')

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data_evento = request.POST.get('data')
        local = request.POST.get('local')
        tipo_id = request.POST.get('tipo_id')
        responsavel = request.POST.get('responsavel')
        horario_evento = request.POST.get('horario_evento')

        # Busca o usuário logado no banco
        usuario = Usuario.objects.get(id=request.session['user_id'])
        tipo = TipoEvento.objects.get(id=tipo_id)

        Evento.objects.create(
            titulo=titulo,
            descricao=descricao,
            data_evento=data_evento,
            local=local,
            tipo=tipo,
            cadastrado_por=usuario,
            responsavel=responsavel,
            horario_evento=horario_evento,

        )
        return redirect('home')

    tipos = TipoEvento.objects.all()
    return render(request, 'cadastro_evento.html', {'tipos': tipos})


def gerenciar_eventos_view(request):
    # Proteção de acesso
    if 'user_id' not in request.session:
        return redirect('login')

    if request.session.get('user_perfil') not in ['Empresa', 'Admin']:
        messages.error(request, 'Acesso negado.')
        return redirect('home')

    if request.method == 'POST':
        acao = request.POST.get('acao')
        evento_id = request.POST.get('id')

        # EXCLUIR EVENTO
        if acao == 'excluir':
            try:
                evento = Evento.objects.get(id=evento_id)
                evento.delete()
                messages.success(request, 'Evento removido com sucesso!')
            except Evento.DoesNotExist:
                messages.error(request, 'Evento não encontrado.')

        # EDITAR EVENTO (ALTERAR)
        elif acao == 'alterar':
            try:
                evento = Evento.objects.get(id=evento_id)
                evento.titulo = request.POST.get('titulo')
                evento.descricao = request.POST.get('descricao')
                evento.data_evento = request.POST.get('data')
                evento.horario_evento = request.POST.get(
                    'horario_evento')  # Nome corrigido
                evento.responsavel = request.POST.get('responsavel')
                evento.local = request.POST.get('local')
                evento.tipo_id = request.POST.get('tipo_id')

                evento.save()
                messages.success(request, 'Evento atualizado com sucesso!')
            except Evento.DoesNotExist:
                messages.error(
                    request, 'Erro ao atualizar: Evento não encontrado.')

        return redirect('gerenciar_eventos')

    # GET - Listagem
    eventos = Evento.objects.all().order_by('-data_evento')
    tipos = TipoEvento.objects.all()

    return render(request, 'gerenciar_eventos.html', {
        'eventos': eventos,
        'tipos': tipos,
    })


def inscrever_evento_view(request):
    if request.method == 'POST' and 'user_id' in request.session:
        evento_id = request.POST.get('evento_id')
        user_id = request.session['user_id']
        user_perfil = request.session.get('user_perfil')

        try:
            evento = Evento.objects.get(id=evento_id)

            # Validação 1: Não permite inscrição em Palestras
            if evento.tipo.nome == 'Palestra':
                messages.error(request, 'Palestras não exigem inscrição.')
                return redirect('home')

            # Validação 2: Mini Curso apenas para Pessoa Comum
            if evento.tipo.nome == 'Mini Curso' and user_perfil != 'Cliente':
                messages.error(
                    request, 'Apenas usuários comuns podem se inscrever em mini cursos.')
                return redirect('home')

            # Se passar nas regras, cria a inscrição
            Inscricao.objects.get_or_create(
                usuario_id=user_id, evento_id=evento_id)
            messages.success(
                request, f'Inscrição em "{evento.titulo}" confirmada!')

        except Evento.DoesNotExist:
            messages.error(request, 'Evento não encontrado.')

        return redirect('home')

    return redirect('login')
