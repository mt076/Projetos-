SELECT * FROM cap15.dsa_campanha_marketing LIMIT 1000;

--Explorando os dados e detectando anomalias

SELECT DISTINCT 
	publico_alvo,
	COUNT(publico_alvo) AS contagem_publico_alvo
FROM cap15.dsa_campanha_marketing
GROUP BY publico_alvo;

--Tratando

UPDATE cap15.dsa_campanha_marketing
SET publico_alvo = 'Outros'
WHERE publico_alvo = '?';

--Pegando a moda da coluna canais_divulgacao

SELECT 
	canais_divulgacao AS canais,
	COUNT(*) AS total
	FROM cap15.dsa_campanha_marketing
GROUP BY canais_divulgacao;

--Optando por tratar o valor NULL com a moda dessa coluna

UPDATE cap15.dsa_campanha_marketing
SET canais_divulgacao = 'Sites de Notícias'
WHERE canais_divulgacao IS NULL;

--Detectando valores ausentes na coluna tipo_campanha

SELECT 
	tipo_campanha AS campanha,
	COUNT(*) AS total
	FROM cap15.dsa_campanha_marketing
GROUP BY tipo_campanha;

--Deletando dados NULL

DELETE FROM cap15.dsa_campanha_marketing
WHERE tipo_campanha IS NULL;

--1) Crie uma query que identifique valores ausentes na coluna Orçamento

SELECT 
	orcamento,
	COUNT(*) AS contagem
FROM cap15.dsa_campanha_marketing
WHERE orcamento IS NULL
GROUP BY orcamento;

--2) Considere  que  orçamento  nulo  para  público  alvo  igual  "Outros"  não  
--seja  uma informação relevante.Crie uma query com delete que remova registros 
--se a coluna orcamento tiver valor ausente e a coluna publico_alvo tiver o valor "Outros"

SELECT 
	publico_alvo,
	orcamento,
	COUNT(*) AS contagem
FROM cap15.dsa_campanha_marketing
WHERE orcamento IS NULL
GROUP BY publico_alvo, orcamento;

DELETE FROM cap15.dsa_campanha_marketing
WHERE publico_alvo = 'Outros' AND orcamento IS NULL; 

--3) Crie uma query que preencha os valores ausentes da coluna orcamento com a média da coluna, 
--mas segmentado pela coluna canais_divulgacao

SELECT
	canais_divulgacao,
	orcamento,
	COUNT(*) AS contagem
FROM cap15.dsa_campanha_marketing
WHERE orcamento IS NULL
GROUP BY canais_divulgacao, orcamento;


UPDATE cap15.dsa_campanha_marketing
SET orcamento = AVG(orcamento)
WHERE orcamento IS NULL;


--4) Use como estratégia de tratamento de outliers criar uma nova coluna e preenchê-la com True se 
--houver outlier no registro e False caso contrário

-- Verificamos outliers novamente:

WITH stats AS (
    SELECT
        AVG(orcamento) AS avg_orcamento,
        STDDEV(orcamento) AS stddev_orcamento,
        AVG(taxa_conversao) AS avg_taxa_conversao,
        STDDEV(taxa_conversao) AS stddev_taxa_conversao,
        AVG(impressoes) AS avg_impressoes,
        STDDEV(impressoes) AS stddev_impressoes
    FROM
        cap16.dsa_campanha_marketing
)
SELECT
    id,
    nome_campanha,
    data_inicio,
    data_fim,
    orcamento,
    publico_alvo,
    canais_divulgacao,
    taxa_conversao,
    impressoes
FROM
    cap16.dsa_campanha_marketing,
    stats
WHERE
    orcamento < (avg_orcamento - 1.5 * stddev_orcamento) OR 
    orcamento > (avg_orcamento + 1.5 * stddev_orcamento) OR
    taxa_conversao < (avg_taxa_conversao - 1.5 * stddev_taxa_conversao) OR 
    taxa_conversao > (avg_taxa_conversao + 1.5 * stddev_taxa_conversao) OR
    impressoes < (avg_impressoes - 1.5 * stddev_impressoes) OR 
    impressoes > (avg_impressoes + 1.5 * stddev_impressoes);

-- Cria a nova coluna

ALTER TABLE cap16.dsa_campanha_marketing
ADD COLUMN tem_outlier BOOLEAN DEFAULT FALSE;

-- Carrega a nova coluna
WITH stats AS (
    SELECT
        AVG(orcamento) AS avg_orcamento,
        STDDEV(orcamento) AS stddev_orcamento,
        AVG(taxa_conversao) AS avg_taxa_conversao,
        STDDEV(taxa_conversao) AS stddev_taxa_conversao,
        AVG(impressoes) AS avg_impressoes,
        STDDEV(impressoes) AS stddev_impressoes
    FROM
        cap16.dsa_campanha_marketing
)
UPDATE cap16.dsa_campanha_marketing
SET tem_outlier = TRUE
FROM stats
WHERE
    orcamento < (avg_orcamento - 1.5 * stddev_orcamento) OR 
    orcamento > (avg_orcamento + 1.5 * stddev_orcamento) OR
    taxa_conversao < (avg_taxa_conversao - 1.5 * stddev_taxa_conversao) OR 
    taxa_conversao > (avg_taxa_conversao + 1.5 * stddev_taxa_conversao) OR
    impressoes < (avg_impressoes - 1.5 * stddev_impressoes) OR 
    impressoes > (avg_impressoes + 1.5 * stddev_impressoes);


-- Verifica os dados:

SELECT * FROM cap16.dsa_campanha_marketing;

SELECT tem_outlier, COUNT(*) AS contagem
FROM cap16.dsa_campanha_marketing
GROUP BY tem_outlier;


--5) Aplique  label  encoding(técnica  de  representação  numérica  de  dados  de  texto)na coluna    
--publico_alvo    e    salve    o    resultado    em    uma    nova    coluna    chamada publico_alvo_encoded

--6) Aplique label encoding na coluna canais_divulgacao e salve o resultado em uma nova coluna chamada canais_divulgacao_encoded

--7) Aplique  label  encoding  na  coluna  tipo_campanha  e  salve  o  resultado  em  uma  nova coluna chamada tipo_campanha_encoded


--Argumento usado no encoding da coluna canais_divulgacao (Maior quantidade)
--Argumento usado no encoding da coluna tipo_campanha (Maior quantidade)

SELECT
	id,
	nome_campanha,
	data_inicio,
	data_fim,
	orcamento,
	publico_alvo,
	canais_divulgacao,
	tipo_campanha,
	taxa_conversao,
	impressoes,
	CASE
		WHEN publico_alvo = 'Publico Alvo 1' THEN 1
		WHEN publico_alvo = 'Publico Alvo 2' THEN 2
		WHEN publico_alvo = 'Publico Alvo 3' THEN 3
		WHEN publico_alvo = 'Publico Alvo 4' THEN 4
		WHEN publico_alvo = 'Publico Alvo 5' THEN 5
	END AS publico_alvo_encoded,
	CASE
		WHEN canais_divulgacao = 'Redes Sociais' THEN 1
		WHEN canais_divulgacao = 'Google' THEN 2
		WHEN canais_divulgacao = 'Sites de Notícias' THEN 3
	END AS canais_divulgacao_encoding,
	CASE
		WHEN tipo_campanha = 'Promocional' THEN 1
		WHEN tipo_campanha = 'Divulgação' THEN 2
		WHEN tipo_campanha = 'Mais Seguidores' THEN 3
	END AS tipo_campanha_encoding
FROM cap15.dsa_campanha_marketing;


--Faça o drop das 3 colunas originais que foram codificadas nos itens 5, 6 e 7

ALTER TABLE cap15.dsa_campanha_marketing
DROP COLUMN tipo_campanha_encoding,
DROP COLUMN canais_divulgacao_encoding,
DROP COLUMN publico_alvo_encoding;


