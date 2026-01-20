# projeto_web_gebov


-- Criar o banco de dados
CREATE DATABASE db_gebov;

-- Criar o usuário
CREATE USER gebov_user WITH PASSWORD 'gebov123';

-- Configurar encoding
ALTER DATABASE db_gebov OWNER TO gebov_user;

-- Dar privilégios ao usuário
GRANT ALL PRIVILEGES ON DATABASE db_gebov TO gebov_user;

-- Conectar ao banco
\c db_gebov

-- Dar privilégios no schema public (necessário para PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO gebov_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gebov_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gebov_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO gebov_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO gebov_user;

-- Sair
\q