from datetime import date, datetime, time
from decimal import Decimal
import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

from .crud import salvar_documento

load_dotenv()

TABELAS = [
    ("usuario", "usuarios", ["cpf"]),
    ("professor", "professores", ["mat_professor"]),
    ("departamento", "departamentos", ["cod_depto"]),
    ("curso", "cursos", ["idcurso"]),
    ("estudante", "estudantes", ["mat_estudante"]),
    ("vinculo", "vinculos", ["idvinculo"]),
    ("projeto", "projetos", ["id_projeto"]),
    ("plano", "planos", ["mat_estudante", "ano"]),
    ("disciplina", "disciplinas", ["cod_disc"]),
    ("semestre", "semestres", ["ano", "semestre"]),
    ("sala", "salas", ["id_sala"]),
    ("horario", "horarios", ["id_horario"]),
    ("turma", "turmas", ["id_turma"]),
    ("leciona", "lecionas", ["id_turma", "mat_professor"]),
    ("alocacao", "alocacoes", ["id_turma", "id_horario"]),
    ("cursa", "cursas", ["mat_estudante", "id_turma"]),
]


def carregar():
    with psycopg.connect(os.getenv("POSTGRES_URL"), row_factory=dict_row) as conexao:
        with conexao.cursor() as cursor:
            for tabela, colecao, campos_chave in TABELAS:
                cursor.execute(f"SELECT * FROM universidade.{tabela}")
                linhas = cursor.fetchall()

                for linha in linhas:
                    documento = dict(linha)

                    for campo in documento:
                        valor = documento[campo]
                        if campo == "cpf" and valor is not None:
                            documento[campo] = str(valor)
                        elif type(valor) is date:
                            documento[campo] = datetime.combine(valor, time())
                        elif type(valor) is Decimal:
                            documento[campo] = float(valor)

                    filtro = {campo: documento[campo] for campo in campos_chave}
                    salvar_documento(colecao, documento, filtro)

                print(f"{colecao}: {len(linhas)} registros")


if __name__ == "__main__":
    carregar()
