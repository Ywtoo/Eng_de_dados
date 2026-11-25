PYTHON ?= python3

.PHONY: help setup env up down logs status check esquema-mongo carregar-mongo mongo-crud

# Mostra os comandos disponíveis.
help:
	@printf '\nComandos:\n\n'
	@printf '  make help   Mostra esta lista.\n'
	@printf '  make setup  Instala o que o Python precisa.\n'
	@printf '  make env    Cria o arquivo .env para acessar os bancos.\n'
	@printf '  make up     Inicia os bancos.\n'
	@printf '  make down   Para os bancos e apaga os dados locais.\n'
	@printf '  make logs   Mostra as mensagens dos bancos.\n'
	@printf '  make status Mostra se os bancos estão ligados.\n'
	@printf '  make check  Confere se o Python acessa os bancos.\n'
	@printf '  make esquema-mongo Cria as coleções e regras do MongoDB.\n'
	@printf '  make carregar-mongo Copia os dados do PostgreSQL para o MongoDB.\n'
	@printf '  make mongo-crud Abre o menu de CRUD do MongoDB.\n'
	@printf '\n'

# Instala os pacotes usados pelo Python.
setup:
	$(PYTHON) -m pip install -r requirements.txt

# Cria o arquivo com os endereços locais, se ainda não existir.
env:
	@test -f .env || cp .env.example .env

# Inicia os bancos. O PostgreSQL carrega o dump na primeira vez.
up:
	docker compose up -d

# Para os bancos e apaga os dados locais.
down:
	docker compose down

logs:
	docker compose logs -f

status:
	docker compose ps

# Confere se o programa acessa os bancos.
check: env
	$(PYTHON) -m app

esquema-mongo: env
	$(PYTHON) -m parte2_mongodb.esquema

carregar-mongo: env
	$(PYTHON) -m parte2_mongodb.carregar_dados

mongo-crud: env
	$(PYTHON) -m parte2_mongodb
