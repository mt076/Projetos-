CREATE TABLE Direcao (
    cod_direcao int PRIMARY KEY,
    cod_titulo int NOT NULL,
    cod_pessoa int NOT NULL
);

CREATE TABLE Autoria (
    cod_autoria int PRIMARY KEY,
    cod_titulo int NOT NULL,
    cod_pessoa int NOT NULL
);

CREATE TABLE Pessoa (
    cod_pessoa int NOT NULL,
    nom_pessoa varchar(500) NOT NULL,
    ano_nascimento int NULL,
    ano_falescimento int NULL,
    dsc_profissao varchar(1000) NULL
);

CREATE TABLE Elenco (
    cod_elenco int PRIMARY KEY,
    cod_titulo int NOT NULL,
    cod_pessoa int NOT NULL,
    dsc_funcao varchar(1000) NOT NULL,
    dsc_personagem varchar(1000) NULL
);

CREATE TABLE Titulo_Detalhe (
    cod_titulo int NOT NULL,
    tip_titulo varchar(100) NOT NULL,
    nom_principal_titulo varchar(1000) NOT NULL,
    nom_original_titulo varchar(1000) NOT NULL,
    id_adulto int NOT NULL,
    ano_lancamento int NOT NULL, 
    qtd_minutos smallint NULL,
    dsc_genero varchar(1000) NULL
);

CREATE TABLE Titulo (
    cod_titulo int NOT NULL,
    nom_titulo varchar(1000) NULL
);

CREATE TABLE Avaliacao (
    cod_titulo int NOT NULL,
    classificacao_media int NOT NULL,
    qtd_votos int NOT NULL
);


ALTER TABLE Pessoa
MODIFY nom_pessoa VARCHAR2(1000);
--Altera dados da tabela Pessoa, modificando a coluna nom_pessoa para varchar(1000).

SELECT 
    p.nom_pessoa,
    t.nom_titulo
FROM 
    Direcao d
INNER JOIN 
    Pessoa p ON d.cod_pessoa = p.cod_pessoa
INNER JOIN 
    Titulo t ON d.cod_titulo = t.cod_titulo;
--Esse script realiza uma consulta SQL que seleciona os nomes das pessoas (nom_pessoa) e os títulos (nom_titulo) associados a elas, com base em uma tabela de relacionamento chamada Direcao.

SELECT COUNT(*)
FROM Titulo
WHERE nom_titulo IS NULL;
--Esse comando vai contar quantos registros na tabela Titulo têm o valor NULL na coluna nom_titulo.

SELECT T.*,D.*
FROM Titulo T JOIN Titulo_Detalhe D
ON T.cod_titulo = D.cod_titulo
ORDER BY T.nom_titulo ASC;
--A query acima retornará à relação dos títulos (e seus detalhes) em ordem alfabética

SELECT T.*, A.*
FROM Titulo T
JOIN Avaliacao A
ON T.cod_titulo = A.cod_titulo
ORDER BY A.classificacao_media DESC
FETCH FIRST 100 ROWS ONLY;
--A query acima retornará à relação dos 100 títulos mais bem avaliados, suas avaliações e total de votos.

SELECT T.*, P.nom_pessoa AS "Autor", P2.nom_pessoa AS "Diretor"
FROM Titulo T
LEFT JOIN Autoria A ON T.cod_titulo = A.cod_titulo
LEFT JOIN Pessoa P ON A.cod_pessoa = P.cod_pessoa
LEFT JOIN Direcao D ON T.cod_titulo = D.cod_titulo
LEFT JOIN Pessoa P2 ON D.cod_pessoa = P2.cod_pessoa
ORDER BY T.nom_titulo
--FETCH FIRST 1000 ROWS ONLY;  <---- vai filtrar só 1000 dados
--Esse script retorna os títulos (T.nom_titulo) e seus respectivos autores e diretores, com base nas tabelas relacionadas, e ordena os resultados pelo nome do título (T.nom_titulo).

SELECT *
FROM Titulo T
LEFT JOIN Avaliacao A ON T.cod_titulo = A.cod_titulo
WHERE A.cod_titulo IS NULL;
--Esse script seleciona todos os registros da tabela Titulo que não possuem correspondência na tabela Avaliacao, ou seja, títulos que ainda não têm avaliação associada.

SELECT *
FROM Titulo T
JOIN Titulo_Detalhe D ON T.cod_titulo = D.cod_titulo
WHERE D.qtd_minutos IS NOT NULL OR D.dsc_genero IS NOT NULL;
--O INNER JOIN entre Titulo e Titulo_Detalhe garante que apenas os títulos com detalhes associados sejam retornados.
--A condição WHERE D.qtd_minutos IS NULL OR D.dsc_genero IS NULL garante que apenas os registros onde pelo menos um dos campos (qtd_minutos ou dsc_genero) seja nulo serão incluídos no resultado.

SELECT *
FROM Titulo T LEFT JOIN Autoria A
ON T.cod_titulo = A.cod_titulo
WHERE A.cod_titulo IS NULL;
--O LEFT JOIN garante que todos os registros da tabela Titulo sejam retornados, mesmo que não haja correspondência na tabela Autoria.
--A condição WHERE A.cod_titulo IS NULL filtra apenas os registros de Titulo que não têm um autor associado, ou seja, títulos sem autor.

SELECT * 
FROM Titulo T LEFT JOIN Elenco E 
ON T.cod_titulo = E.cod_titulo 
WHERE E.cod_titulo IS NULL;
--O LEFT JOIN retorna todos os registros da tabela Titulo e os registros correspondentes da tabela Elenco. Se não houver correspondência na tabela Elenco para algum título, os campos relacionados ao Elenco serão NULL.
--A condição WHERE E.cod_titulo IS NULL filtra para retornar apenas os títulos que não têm elenco associado.

SELECT * FROM pessoa
WHERE ROWNUM <= 22;
--Seleciona os primeiros 22 registros.


SELECT *
FROM Titulo T LEFT JOIN Autoria A
ON T.cod_titulo = A.cod_titulo
WHERE A.cod_titulo IS NULL;
--retornar a lista de títulos sem avaliação

SELECT *
FROM Titulo T JOIN Titulo_Detalhe D
ON T.cod_titulo = D.cod_titulo
WHERE D.qtd_minutos IS NULL AND D.dsc_genero IS NULL;
--retornará os títulos sem o detalhe da duração ou informação do gênero (dsc_genero)

SELECT *
FROM Titulo T LEFT JOIN Direcao D
ON T.cod_titulo = D.cod_titulo
WHERE D.cod_titulo IS NULL;
--retornará os títulos sem diretor

SELECT *
FROM Titulo T LEFT JOIN Elenco E
ON T.cod_titulo = E.cod_titulo
WHERE E.cod_titulo IS NULL;
--retornará os títulos sem elenco

SELECT T.nom_titulo AS "Nome do Título", 
       UPPER(TD.tip_titulo) AS "Tipo do Título", 
       TD.ano_lancamento AS "Ano de Lançamento", 
       TD.qtd_minutos AS "Duração", 
       TD.dsc_genero AS "Gênero(s)", 
       A.classificacao_media AS "Nota", 
       P.nom_pessoa AS "Autor", 
       P2.nom_pessoa AS "Diretor"
FROM Titulo T 
LEFT JOIN Titulo_Detalhe TD ON T.cod_titulo = TD.cod_titulo
LEFT JOIN Avaliacao A ON T.cod_titulo = A.cod_titulo
LEFT JOIN Autoria E ON T.cod_titulo = E.cod_titulo
LEFT JOIN Pessoa P ON E.cod_pessoa = P.cod_pessoa
LEFT JOIN Direcao D ON T.cod_titulo = D.cod_titulo
LEFT JOIN Pessoa P2 ON D.cod_pessoa = P2.cod_pessoa
ORDER BY T.nom_titulo;
--ativos, ordenados alfabeticamente pelo nome do título, com seu(s) autor(es) e diretor(es)


















