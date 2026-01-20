# GEBOV - Sistema de Gestão de Eventos

Este projeto é uma plataforma de gestão de eventos desenvolvida em **Django 5.0**, com foco na simplicidade de uso e controle rigoroso de perfis de acesso. O sistema permite o cadastro de usuários, gerenciamento de eventos por administradores/gerentes e inscrições para participantes.

---

## 🛠 Tecnologias Utilizadas

- **Framework:** Django 5.0
- **Banco de Dados:** PostgreSQL
- **Estilização:** Tailwind CSS (via CDN)
- **Interatividade:** Alpine.js
- **Configuração:** Python-Decouple (Variáveis de ambiente)
- **Segurança:** PBKDF2 (Hashing de senhas)

---

## 🚀 Guia de Instalação

### 1. Requisitos Prévios
Certifique-se de ter o **Python 3.10+** e o **PostgreSQL** instalados.

### 2. Configuração do Ambiente
```bash
# Clone o repositório
git clone [https://github.com/LaisOliveiira/projeto_web_gebov](https://github.com/LaisOliveiira/projeto_web_gebov)
cd projeto_web_gebov

# Crie e ative o ambiente virtual
python -m venv venv
# Windows: venv\Scripts\activate | Linux: source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
Com as informações completas, compilei toda a lógica do seu projeto em um guia de documentação técnica. Este conteúdo é ideal para o seu `README.md` ou para compor a documentação oficial do projeto **GEBOV**.

---

### 3. Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True

DB_NAME=db_gebov
DB_USER=gebov_user
DB_PASSWORD=gebov123
DB_HOST=localhost
DB_PORT=5432

```

### 4. Banco de Dados e Inicialização

Execute os comandos no terminal do PostgreSQL para criar o banco, e então rode as migrações:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

---

## 🔑 Fluxo de Autenticação e Perfis

O sistema utiliza **Django Sessions** para controle de acesso, com três perfis principais:

1. **Admin:** Acesso total. Gerencia a base de usuários (lista_usuarios) e pode promover um usuário comum ao perfil de **Empresa/Gerente** alterando seu atributo de perfil.
2. **Empresa (Gerente):** Pode cadastrar novos eventos e gerenciar (editar/excluir) todos os eventos da plataforma.
3. **Cliente (Pessoa Comum):** Pode se cadastrar no sistema, visualizar eventos na Home e se inscrever em **Mini Cursos**.

---

## 📁 Documentação das Views (Lógica de Negócio)

### App Autenticação

* **`login_view`**: Autentica o usuário pelo e-mail e armazena `user_id`, `user_nome` e `user_perfil` na sessão.
* **`cadastro_usuario_view`**: Permite o auto-cadastro de novos usuários. Por padrão, todo novo cadastro recebe o perfil **"Pessoa Comum"**.
* **`lista_usuarios`**: (Restrito ao Admin) Permite a listagem completa de usuários, edição de dados/perfis e exclusão de contas.

### App Eventos

* **`cadastro_evento_view`**: (Admin/Empresa) Formulário para criação de novos eventos vinculando o usuário que cadastrou.
* **`gerenciar_eventos_view`**: (Admin/Empresa) Lista todos os eventos com opções de edição e exclusão via requisições `POST` com campos de `acao`.
* **`inscrever_evento_view`**: (Cliente) Processa a inscrição de participantes.
* *Regra:* Não permite inscrição em "Palestras" (acesso livre).
* *Regra:* Apenas perfis "Cliente" podem se inscrever em "Mini Cursos".



---

## 📂 Estrutura de Rotas (URLs)

### Autenticação (`/auth/`)

| Rota | Nome | Descrição |
| --- | --- | --- |
| `/` | `login` | Tela de login |
| `/home/` | `home` | Dashboard principal |
| `/logout/` | `logout` | Encerra a sessão |
| `/lista_usuarios/` | `lista_usuarios` | Gestão de usuários (Admin) |

### Eventos (`/eventos/`)

| Rota | Nome | Descrição |
| --- | --- | --- |
| `/cadastro/` | `cadastro_evento` | Criar novo evento |
| `/gerenciar/` | `gerenciar_eventos` | Editar/Excluir eventos |
| `/inscrever/` | `inscrever_evento` | Inscrição de participantes |

---
