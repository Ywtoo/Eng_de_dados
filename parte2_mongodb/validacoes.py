from .crud import banco


def validar_referencias(colecao, documento):
    if colecao == "estudantes" and documento.get("cpf") is not None:
        if not banco.usuarios.find_one({"cpf": documento["cpf"]}):
            raise ValueError("Esse usuário não existe.")

    if colecao == "vinculos":
        matricula = documento.get("mat_estudante")
        if matricula is not None and not banco.estudantes.find_one({"mat_estudante": matricula}):
            raise ValueError("Esse estudante não existe.")

        curso = documento.get("curso")
        if curso is not None and not banco.cursos.find_one({"idcurso": curso}):
            raise ValueError("Esse curso não existe.")


def impedir_exclusao_com_referencias(colecao, documento):
    if colecao == "usuarios":
        cpf = documento["cpf"]
        if banco.estudantes.find_one({"cpf": cpf}) or banco.professores.find_one({"cpf": cpf}):
            raise ValueError("Esse usuário está ligado a um estudante ou professor.")

    if colecao == "estudantes":
        matricula = documento["mat_estudante"]
        if banco.vinculos.find_one({"mat_estudante": matricula}):
            raise ValueError("Esse estudante tem vínculos cadastrados.")
        if banco.planos.find_one({"mat_estudante": matricula}) or banco.cursas.find_one({"mat_estudante": matricula}):
            raise ValueError("Esse estudante aparece em planos ou turmas.")

    if colecao == "cursos":
        if banco.vinculos.find_one({"curso": documento["idcurso"]}):
            raise ValueError("Esse curso está ligado a um vínculo.")
