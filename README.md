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
