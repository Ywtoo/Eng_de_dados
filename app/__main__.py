"""Confere se o Python consegue acessar os bancos."""

import os

import psycopg
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

with psycopg.connect(os.getenv("POSTGRES_URL")):
    print("PostgreSQL conectado")

with MongoClient(os.getenv("MONGO_URL"), serverSelectionTimeoutMS=5000) as mongo:
    mongo.admin.command("ping")
    print("MongoDB conectado")
