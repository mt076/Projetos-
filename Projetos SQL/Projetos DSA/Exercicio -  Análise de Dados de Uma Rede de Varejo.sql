1. Qual o Número Total de Vendas e Média de Quantidade Vendida?

SELECT
	COUNT(quantidade) AS numero_de_vendas,
	ROUND(AVG(quantidade), 2) AS media_quantidade_vendas
FROM cap17.vendas;


2. Qual o Número Total de Produtos Únicos Vendidos?

SELECT COUNT(DISTINCT id_produto) FROM cap17.vendas;

SELECT
	COALESCE(nome, 'total'),
	COUNT(*) AS quantidade
FROM cap17.produtos
GROUP BY 
	ROLLUP(nome)
ORDER BY quantidade ASC;

3. Quantas Vendas Ocorreram Por Produto? Mostre o Resultado em Ordem Decrescente.

SELECT 
	P.nome,
	COUNT(V.id_produto) AS quantidade_vendida,
FROM cap17.vendas AS V
INNER JOIN cap17.produtos AS P ON V.id_produto = P.id_produto
GROUP BY P.nome
ORDER BY quantidade_vendida DESC;

4. Quais os 5 Produtos com Maior Número de Vendas?

SELECT 
	P.nome,
	COUNT(*) AS total_vendas
FROM cap17.vendas AS V
INNER JOIN cap17.produtos AS P ON V.id_produto = P.id_produto
GROUP BY P.nome
ORDER BY total_vendas DESC
LIMIT 5;

5. Quais Clientes Fizeram 6 ou Mais Transações de Compra?
	
SELECT
	C.nome,
	COUNT(V.id_produto) AS total_compras
FROM cap17.vendas AS V
INNER JOIN cap17.clientes AS C ON V.id_cliente = C.id_cliente
GROUP BY C.nome
HAVING COUNT(V.id_produto) >= 6
ORDER BY total_compras DESC;

6. Qual o Total de Transações Comerciais Por Mês no Ano de 2024? Apresente os Nomes 
dos Meses no Resultado, Que Deve Ser Ordenado Por Mês.

SELECT
	EXTRACT(YEAR FROM data_venda) AS ano,
	CASE
		WHEN EXTRACT(MONTH FROM data_venda) = 1 THEN '01-Janeiro'
    	WHEN EXTRACT(MONTH FROM data_venda) = 2 THEN '02-Fevereiro'
    	WHEN EXTRACT(MONTH FROM data_venda) = 3 THEN '03-Março'  
    	WHEN EXTRACT(MONTH FROM data_venda) = 4 THEN '04-Abril'
    	WHEN EXTRACT(MONTH FROM data_venda) = 5 THEN '05-Maio'  
    	WHEN EXTRACT(MONTH FROM data_venda) = 6 THEN '06-Junho'
    	WHEN EXTRACT(MONTH FROM data_venda) = 7 THEN '07-Julho'
    	WHEN EXTRACT(MONTH FROM data_venda) = 8 THEN '08-Agosto'
    	WHEN EXTRACT(MONTH FROM data_venda) = 9 THEN '09-Setembro'
    	WHEN EXTRACT(MONTH FROM data_venda) = 10 THEN '10-Outubro'
    	WHEN EXTRACT(MONTH FROM data_venda) = 11 THEN '11-Novembro'
    	WHEN EXTRACT(MONTH FROM data_venda) = 12 THEN '12-Dezembro'
	END AS mes,
	COUNT(*) AS total_vendas
FROM cap17.vendas AS V
INNER JOIN cap17.produtos AS P ON V.id_produto = P.id_produto
WHERE EXTRACT(YEAR FROM data_venda) = (2024)
GROUP BY EXTRACT(YEAR FROM data_venda), EXTRACT(MONTH FROM data_venda)
ORDER BY mes;

7. Quantas Vendas de Notebooks Ocorreram em Junho e Julho de 2023?

SELECT
	COUNT(*) AS total_vendas
FROM cap17.vendas AS V
INNER JOIN cap17.produtos AS P ON V.id_produto = P.id_produto
WHERE EXTRACT(YEAR FROM data_venda) = (2023) AND EXTRACT(MONTH FROM data_venda) IN (6, 7) AND P.nome = 'Notebook';


8. Qual o Total de Vendas Por Mês e Por Ano ao Longo do Tempo?

SELECT
	DATE_TRUNC('MONTH', data_venda) AS mes,
	COUNT(*) AS total_vendas
FROM cap17.vendas
GROUP BY mes
ORDER BY mes;

9. Quais Produtos Tiveram Menos de 100 Transações de Venda?

SELECT
	P.nome AS produto,
	COUNT(V.id_produto) AS total_vendas
FROM cap17.vendas AS V
INNER JOIN cap17.produtos AS P ON V.id_produto = P.id_produto
GROUP BY P.nome
HAVING COUNT(V.id_produto) < 100
ORDER BY total_vendas;
	
10. Quais Clientes Compraram Smartphone e Também Compraram Smartwatch?

WITH compradores_smartphone AS (
	SELECT
		v.id_produto
	FROM cap17.vendas AS V
	INNER JOIN cap17.produtos AS P ON V.id_produto = P.id_produto
	WHERE p.nome = 'Smartphone'
	GROUP BY v.id_produto
),
compradores_smartwatch AS (
	SELECT
		v.id_cliente
	FROM cap17.vendas AS V
	INNER JOIN cap17.produtos AS P ON V.id_produto = P.id_produto
	WHERE p.nome = 'Smartwatch'
	GROUP BY v.id_cliente
)
SELECT
	C.nome
FROM cap17.clientes AS C 
WHERE C.id_cliente IN (
	SELECT 
		id_cliente
	FROM compradores_smartphone
	INTERSECT
	SELECT
		id_cliente
	FROM compradores_smartwatch
);

11. Quais Clientes Compraram Smartphone e Também Compraram Smartwatch, Mas Não 
Compraram Notebook?

WITH compradores_smartphone AS (
	SELECT
		v.id_produto
	FROM cap17.vendas AS V
	INNER JOIN cap17.produtos AS P ON V.id_produto = P.id_produto
	WHERE p.nome = 'Smartphone'
	GROUP BY v.id_produto
),
compradores_smartwatch AS (
	SELECT
		v.id_cliente
	FROM cap17.vendas AS V
	INNER JOIN cap17.produtos AS P ON V.id_produto = P.id_produto
	WHERE p.nome = 'Smartwatch'
	GROUP BY v.id_cliente
),
clientes_notebook AS (
	SELECT
		v.id_cliente
	FROM cap17.vendas AS V
	INNER JOIN cap17.produtos AS P ON V.id_produto = P.id_produto
	WHERE p.nome = 'Notebook'
	GROUP BY v.id_cliente
)
SELECT
	clientes.nome
FROM cap17.clientes
WHERE clientes.id_cliente IN (
	SELECT id_cliente
	FROM compradores_smartphone
	INTERSECT
	SELECT id_cliente
	FROM compradores_smartwatch
)
AND id_cliente NOT IN (
	SELECT id_cliente FROM clientes_notebook
);


12. Quais Clientes Compraram Smartphone e Também Compraram Smartwatch, Mas Não 
Compraram Notebook em Maio/2024?

WITH clientes_smartphone AS (
	SELECT
		id_cliente
	FROM cap17.vendas
	INNER JOIN cap17.produtos ON vendas.id_produto = produtos.id_produto
	WHERE produtos.nome = 'Smartphone'
	AND DATE_PART('year', vendas.data_venda) = 2024
	AND DATE_PART('month', vendas.data_venda) = 5
),
clientes_smartwatch AS (
	SELECT
		vendas.id_cliente
	FROM cap17.vendas
	INNER JOIN cap17.produtos ON vendas.id_produto = produtos.id_produto
	WHERE produtos.nome = 'Smartwatch'
	AND DATE_PART('year', vendas.data_venda) = 2024
	AND DATE_PART('month', vendas.data_venda) = 5
),
clientes_notebook AS (
	SELECT
		vendas.id_cliente
	FROM cap17.vendas
	INNER JOIN cap17.produtos ON vendas.id_produto = produtos.id_produto
	WHERE produtos.nome = 'Notebook'
	AND DATE_PART('year', vendas.data_venda) = 2024
	AND DATE_PART('month', vendas.data_venda) = 5
)
SELECT
	clientes.nome
FROM cap17.clientes
WHERE clientes.id_cliente IN (
	SELECT id_cliente
	FROM clientes_smartphone
	INTERSECT
	SELECT id_cliente
	FROM clientes_smartwatch
)
AND id_cliente NOT IN (
	SELECT id_cliente FROM clientes_notebook
);


13. Qual a Média Móvel de Quantidade de Unidades Vendidas ao Longo do Tempo? 
Considere Janela de 7 Dias.

SELECT
	data_venda,
	ROUND(AVG(quantidade) OVER (ORDER BY data_venda ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING),2) AS media_movel_7dias
FROM cap17.vendas
ORDER BY data_venda;

14. Qual a Média Móvel e Desvio Padrão Móvel de Quantidade de Unidades Vendidas ao 
Longo do Tempo? Considere Janela de 7 Dias.

SELECT
	data_venda,
	quantidade,
	ROUND(AVG(quantidade) OVER (ORDER BY data_venda ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING),2) AS media_movel_7dias,
	ROUND(STDDEV(quantidade) OVER (ORDER BY data_venda ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING), 2) AS desvio_padrao_7dias
FROM cap17.vendas
ORDER BY data_venda;

15. Quais Clientes Estão Cadastrados, Mas Ainda Não Fizeram Transação?

SELECT
	C.id_cliente,
	C.nome AS cliente
FROM cap17.vendas AS V
RIGHT JOIN cap17.clientes AS C ON V.id_cliente = C.id_cliente
WHERE V.id_cliente IS NULL;
	

SELECT * FROM cap17.clientes;
SELECT * FROM cap17.produtos;
SELECT * FROM cap17.vendas;
