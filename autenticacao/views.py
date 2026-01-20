from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from eventos.models import Evento, Inscricao


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            # 1. Busca o usuário apenas pelo e-mail
            usuario = Usuario.objects.get(email=email)

            # 2. Verifica a senha
            if usuario.verificar_senha(senha):
                # 3. Login bem-sucedido - Salva na sessão
                request.session['user_id'] = usuario.id
                request.session['user_nome'] = usuario.nome

                # O sistema agora identifica o perfil automaticamente do banco
                request.session['user_perfil'] = usuario.perfil.nome

                return redirect('home')
            else:
                messages.error(request, 'Senha incorreta')
                return render(request, 'login.html')

        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado')
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def cadastro_usuario_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmacao = request.POST.get('confirmacao')

        if senha != confirmacao:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'cadastro_usuario.html')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'cadastro_usuario.html')

        try:
            # CORREÇÃO: Busca ou cria o objeto Perfil para satisfazer a ForeignKey
            perfil_comum, _ = Perfil.objects.get_or_create(nome='Pessoa Comum')

            novo_usuario = Usuario(
                nome=nome,
                email=email,
                perfil=perfil_comum  # Atribui o objeto Perfil
            )
            novo_usuario.senha = senha
            novo_usuario.save()  # O hash é feito no save() do seu model

            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, 'Erro interno ao criar conta.')
            return render(request, 'cadastro_usuario.html')

    return render(request, 'cadastro_usuario.html')

# --- PERFIL E HOME ---


def home_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    # Buscar todos os eventos e os tipos relacionados
    eventos = Evento.objects.select_related(
        'tipo').all().order_by('data_evento')

    # Buscar IDs dos eventos que o usuário já está inscrito
    inscricoes_usuario = Inscricao.objects.filter(
        usuario_id=request.session['user_id']
    ).values_list('evento_id', flat=True)

    context = {
        'nome': request.session.get('user_nome'),
        'perfil': request.session.get('user_perfil'),
        'eventos': eventos,
        'inscricoes_usuario': inscricoes_usuario,
    }
    return render(request, 'home.html', context)


def alterar_senha_view(request):
    if 'user_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmacao = request.POST.get('confirmacao')

        try:
            usuario = Usuario.objects.get(id=request.session['user_id'])

            # 1. Verificar se a senha atual está correta
            if not usuario.verificar_senha(senha_atual):
                messages.error(request, 'Sua senha atual está incorreta.')

            # 2. Verificar se a nova senha e a confirmação batem
            elif nova_senha != confirmacao:
                messages.error(
                    request, 'A nova senha e a confirmação não coincidem.')

            # 3. Sucesso: Atualizar a senha
            else:
                usuario.senha = nova_senha
                usuario.save()
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('home')
        except Usuario.DoesNotExist:
            return redirect('login')

    return render(request, 'alterar_senha.html')


def lista_usuarios(request):
    # Proteção de acesso: Somente Admin entra
    if request.session.get('user_perfil') != 'Admin':
        messages.error(request, 'Acesso negado.')
        return redirect('home')

    if request.method == "POST":
        acao = request.POST.get('acao')
        usuario_id = request.POST.get('id')

        if acao == 'excluir':
            try:
                if int(usuario_id) == request.session.get('user_id'):
                    messages.error(
                        request, 'Você não pode excluir sua própria conta.')
                else:
                    Usuario.objects.get(id=usuario_id).delete()
                    messages.success(request, 'Usuário removido com sucesso!')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuário não encontrado.')

        elif acao == 'alterar':
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                usuario.nome = request.POST.get('nome')
                usuario.email = request.POST.get('email')

                # Atualiza o perfil (é aqui que ocorre a promoção para Gerente/Empresa)
                perfil_id = request.POST.get('perfil_id')
                usuario.perfil_id = perfil_id

                usuario.save()
                messages.success(
                    request, f'Usuário {usuario.nome} atualizado com sucesso!')
            except Usuario.DoesNotExist:
                messages.error(
                    request, 'Erro ao atualizar: Usuário não encontrado.')

        return redirect('lista_usuarios')

    # GET - Listagem ordenada por nome
    usuarios = Usuario.objects.all().select_related('perfil').order_by('nome')
    perfis = Perfil.objects.all()

    return render(request, 'lista_usuarios.html', {
        'usuarios': usuarios,
        'perfis': perfis
    })
