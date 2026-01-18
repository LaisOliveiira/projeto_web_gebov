from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib import messages

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
                return render(request, 'login.html', {'erro': 'Senha incorreta'})

        except Usuario.DoesNotExist:
            return render(request, 'login.html', {'erro': 'Usuário não encontrado'})

    return render(request, 'login.html')

def home_view(request):
    # Proteção: Se não houver id na sessão, volta para o login
    if 'user_id' not in request.session:
        return redirect('login')
    
    # Passamos os dados da sessão para o template
    context = {
        'nome': request.session.get('user_nome'),
        'perfil': request.session.get('user_perfil'),
    }
    return render(request, 'home.html', context)

def logout_view(request):
    # O flush limpa absolutamente tudo da sessão e gera um novo ID de sessão
    request.session.flush()
    return redirect('login')

def alterar_senha_view(request):
    # Proteção de acesso: só logados entram
    if 'user_id' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmacao = request.POST.get('confirmacao')

        usuario = Usuario.objects.get(id=request.session['user_id'])

        # 1. Verificar se a senha atual está correta
        if not usuario.verificar_senha(senha_atual):
            messages.error(request, 'Sua senha atual está incorreta.')
        
        # 2. Verificar se a nova senha e a confirmação batem
        elif nova_senha != confirmacao:
            messages.error(request, 'A nova senha e a confirmação não coincidem.')
        
        # 3. Sucesso: Atualizar a senha
        else:
            usuario.senha = nova_senha # O método save() do model fará o hash automático
            usuario.save()
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('home')

    return render(request, 'alterar_senha.html')