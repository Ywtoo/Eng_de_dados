import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
banco = MongoClient(
    os.getenv("MONGO_URL")
)[os.getenv("MONGO_DATABASE", "universidade")]

with open(Path(__file__).with_name("esquema.json"), encoding="utf-8") as arquivo:
    esquemas = json.load(arquivo)

for nome, regras in esquemas.items():
    if nome in banco.list_collection_names():
        banco.command("collMod", nome, validator=regras)
    else:
        banco.create_collection(nome, validator=regras)

CHAVES = [
    ("usuarios", ["cpf"], None),
    ("usuarios", ["login"], {"login": {"$type": "string"}}),
    ("professores", ["mat_professor"], None),
    ("professores", ["cpf"], {"cpf": {"$type": "string"}}),
    ("departamentos", ["cod_depto"], None),
    ("cursos", ["idcurso"], None),
    ("cursos", ["nome", "turno", "campus", "nivel"], {"campus": {"$type": "string"}, "nivel": {"$type": "string"}}),
    ("estudantes", ["mat_estudante"], None),
    ("estudantes", ["cpf"], {"cpf": {"$type": "string"}}),
    ("vinculos", ["idvinculo"], None),
    ("projetos", ["id_projeto"], None),
    ("planos", ["mat_estudante", "ano"], None),
    ("disciplinas", ["cod_disc"], None),
    ("semestres", ["ano", "semestre"], None),
    ("salas", ["id_sala"], None),
    ("horarios", ["id_horario"], None),
    ("turmas", ["id_turma"], None),
    ("turmas", ["cod_disc", "numero", "semestre", "ano"], {"numero": {"$type": "int"}, "semestre": {"$type": "int"}, "ano": {"$type": "int"}}),
    ("lecionas", ["id_turma", "mat_professor"], None),
    ("alocacoes", ["id_turma", "id_horario"], None),
    ("alocacoes", ["id_horario", "id_sala"], {"id_sala": {"$type": "int"}}),
    ("cursas", ["mat_estudante", "id_turma"], None),
]

for colecao, campos, filtro in CHAVES:
    campos = [(campo, 1) for campo in campos]
    if filtro:
        banco[colecao].create_index(campos, unique=True, partialFilterExpression=filtro)
    else:
        banco[colecao].create_index(campos, unique=True)
