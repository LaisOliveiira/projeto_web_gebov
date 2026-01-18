from django.shortcuts import render, redirect
from .models import Evento, TipoEvento
from autenticacao.models import Usuario
from django.contrib import messages

def cadastro_evento_view(request):
    # Proteção de acesso (Padrão Lumon)
    if 'user_id' not in request.session:
        messages.warning(request, 'Você precisa fazer login primeiro.')
        return redirect('login')


    if request.session.get('user_perfil') != 'Empresa':
        messages.error(request, 'Acesso negado. Apenas administradores podem cadastrar eventos.')
        return redirect('home')

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data_evento = request.POST.get('data')
        local = request.POST.get('local')
        tipo_id = request.POST.get('tipo_id')
        responsavel=request.POST.get('responsavel')
        horario_evento=request.POST.get('horario_evento')


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