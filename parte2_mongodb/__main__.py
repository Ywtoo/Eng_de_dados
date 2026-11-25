import json

from pymongo.errors import PyMongoError

from .crud import (
    apagar_documento,
    atualizar_documento,
    banco,
    consultar_documentos,
    inserir_documento,
)
from .validacoes import impedir_exclusao_com_referencias, validar_referencias

ESTRUTURAS = {
    "1": ("usuário", "usuarios", "cpf"),
    "2": ("estudante", "estudantes", "mat_estudante"),
    "3": ("vínculo", "vinculos", "idvinculo"),
    "4": ("curso", "cursos", "idcurso"),
}


def ler_objeto(mensagem):
    objeto = json.loads(input(mensagem))
    if type(objeto) is not dict:
        raise ValueError("Digite um objeto JSON, por exemplo: {\"cpf\": \"123\"}.")
    return objeto


def mostrar(valor):
    print(json.dumps(valor, ensure_ascii=False, indent=2, default=str))


def executar():
    while True:
        print("\nMongoDB — CRUD")
        print("1. Usuário   2. Estudante   3. Vínculo   4. Curso   0. Sair")
        escolha = input("Escolha: ").strip()
        if escolha == "0":
            break
        if escolha not in ESTRUTURAS:
            print("Opção inválida.")
            continue

        nome, colecao, chave = ESTRUTURAS[escolha]
        operacao = input("1. Inserir  2. Consultar  3. Atualizar  4. Apagar: ").strip()

        try:
            if operacao == "1":
                documento = ler_objeto(f"Dados de {nome} em JSON: ")
                validar_referencias(colecao, documento)
                resultado = inserir_documento(colecao, documento)
                print(f"Inserido com _id {resultado.inserted_id}.")

            elif operacao == "2":
                filtro = ler_objeto("Filtro em JSON (ou {} para listar tudo): ")
                mostrar(consultar_documentos(colecao, filtro))

            elif operacao == "3":
                filtro = ler_objeto("Filtro para localizar o registro em JSON: ")
                documento = banco[colecao].find_one(filtro)
                if documento is None:
                    print("Registro não encontrado.")
                    continue
                campos = ler_objeto("Campos que serão alterados em JSON: ")
                if chave in campos and campos[chave] != documento[chave]:
                    raise ValueError("Não altere a chave principal do registro.")
                documento.update(campos)
                validar_referencias(colecao, documento)
                resultado = atualizar_documento(colecao, filtro, campos)
                print("Registro atualizado." if resultado.modified_count else "Nenhuma mudança feita.")

            elif operacao == "4":
                filtro = ler_objeto("Filtro para localizar o registro em JSON: ")
                documento = banco[colecao].find_one(filtro)
                if documento is None:
                    print("Registro não encontrado.")
                    continue
                impedir_exclusao_com_referencias(colecao, documento)
                apagar_documento(colecao, filtro)
                print("Registro apagado.")

            else:
                print("Opção inválida.")

        except (ValueError, PyMongoError) as erro:
            print(f"Não foi possível concluir: {erro}")


if __name__ == "__main__":
    executar()
