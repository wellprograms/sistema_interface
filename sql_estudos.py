from classes import OperadorCaixa

import mysql.connector

# Estabelecer conexão com o banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="well97",
    database="loja_bd"
)
cursor = conn.cursor()

# Consultar todos os produtos associados à compra com o ID 1
id_compra = 26

# SELECT row 1 : SELECIONANDO COLUNAS ESPECIFICAS DA TABELA produtos_venda

# FROM row 2 : dando um "apelido" a tabela produtos_venda

# JOIN row 3: Realiza uma junção (join)
# com a tabela "vendas" usando a condição de igualdade pv.id_compra = v.id_compra.
# Essa junção permite combinar registros das duas tabelas com base nos valores correspondentes da coluna "id_compra".

# WHERE v.id_compra = %s: Define uma cláusula de filtro para restringir os resultados apenas para as linhas onde o valor da coluna
# "id_compra" na tabela "vendas" seja igual ao valor fornecido (representado por %s). O operador %s é geralmente usado como marcador
#  de posição para valores a serem substituídos posteriormente por meio de um parâmetro, como uma boa prática para evitar ataques de injeção de SQL.


query = """
SELECT pv.id_produto, pv.id_compra, pv.referencia, pv.modelo, pv.genero, pv.quantidade, pv.valor 
FROM produtos_venda pv
JOIN vendas v ON pv.id_compra = v.id_compra
WHERE v.id_compra = %s
"""
cursor.execute(query, (id_compra,))
results = cursor.fetchall()

if results:
    print(f"Produtos da compra com ID {id_compra}:")
    for row in results:
        id_produto, id_compra, referencia, modelo, genero, quantidade, valor = row
        print(f"ID do Produto: {id_produto}")
        print(f"Referência: {referencia}")
        print(f"Modelo: {modelo}")
        print(f"Gênero-: {genero}")
        print(f"Quantidade: {quantidade}")
        print(f"Valor: {valor}")
        print("-----")
else:
    print(f"Compra com ID {id_compra} não encontrada ou não possui produtos associados")

# Fechar a conexão com o banco de dados
conn.close()
