import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

nome_banco = os.getenv("MONGO_DATABASE", "universidade")
cliente = MongoClient(os.getenv("MONGO_URL"))
banco = cliente[nome_banco]


def inserir_documento(nome_colecao, documento):
    return banco[nome_colecao].insert_one(documento)


def salvar_documento(nome_colecao, documento, filtro):
    return banco[nome_colecao].update_one(filtro, {"$set": documento}, upsert=True)


def consultar_documentos(nome_colecao, filtro=None):
    return list(banco[nome_colecao].find(filtro or {}))


def atualizar_documento(nome_colecao, filtro, campos):
    return banco[nome_colecao].update_one(filtro, {"$set": campos})


def apagar_documento(nome_colecao, filtro):
    return banco[nome_colecao].delete_one(filtro)
