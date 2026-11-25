# Parte 2 — MongoDB

## Pesquisa e modelo

Bancos NoSQL podem guardar dados como pares de chave e valor, documentos, colunas ou grafos. Para esta parte do trabalho, o banco definido é o MongoDB, que armazena documentos BSON em coleções e permite consultá-los com MQL.

Para manter o mapeamento fácil de conferir, cada tabela do script `universidade` corresponde a uma coleção MongoDB, e cada linha corresponde a um documento. As chaves que relacionam tabelas continuam como campos nos documentos.

## Restrições

- **Chaves:** índices únicos representam as chaves primárias e restrições `UNIQUE`. Por exemplo, `usuarios.cpf` é único; em `semestres`, a combinação de `ano` e `semestre` é única.
- **Campos obrigatórios e domínios:** `esquema.json` define tipos, campos obrigatórios e valores permitidos. `esquema.py` aplica essas regras às coleções.
- **Integridade referencial:** os registros copiados vêm do PostgreSQL, que já confere as referências. No CRUD, o Python confere usuário do estudante e estudante/curso do vínculo, e impede apagar esses registros enquanto estiverem em uso.

## Carga e CRUD

`carregar_dados.py` lê as tabelas do PostgreSQL e grava os documentos nas coleções correspondentes. `make mongo-crud` abre o programa de terminal com as operações de inserir, consultar, atualizar e apagar para usuário, estudante, vínculo e curso.

Na apresentação, cada operação será executada pelo menu e seu efeito será mostrado na coleção correspondente no MongoDB Compass.

Digite estes documentos ao escolher **Inserir**:

- Usuário: `{"cpf":"99999999999","nome":"Usuario de teste"}`
- Curso: `{"idcurso":9001,"nome":"Curso de teste","turno":"Noturno"}`
- Estudante: `{"mat_estudante":"T999999","cpf":"99999999999"}`
- Vínculo: `{"idvinculo":9001,"mat_estudante":"T999999","curso":9001,"status":"Ativo"}`

Ao escolher **Consultar**, use estes filtros:

- Usuário: `{"cpf":"99999999999"}`
- Curso: `{"idcurso":9001}`
- Estudante: `{"mat_estudante":"T999999"}`
- Vínculo: `{"idvinculo":9001}`

Para **Atualizar**, informe um filtro e depois os campos novos. Exemplo: filtro `{"cpf":"99999999999"}` e campos `{"nome":"Usuario atualizado"}`.

Para **Apagar**, use os mesmos filtros da consulta. Apague nesta ordem para não deixar referências quebradas: vínculo, estudante, usuário e curso.

## Fontes

- [MongoDB: bancos e coleções](https://www.mongodb.com/docs/manual/core/databases-and-collections/)
- [MongoDB: linguagem MQL](https://www.mongodb.com/docs/manual/reference/mql/)
- [MongoDB: validação com JSON Schema](https://www.mongodb.com/docs/manual/core/schema-validation/specify-json-schema/)
- [MongoDB: índices únicos](https://www.mongodb.com/docs/manual/core/index-unique/)
