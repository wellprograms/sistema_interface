import mysql.connector

# Conectando ao banco de dados
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='well97',
    database='db_sistema'
)

import mysql.connector


# Criar cursor para executar as consultas
cursor = conexao.cursor()

# ID do vendedor para realizar a consulta
id_vendedor = 1  # Insira o ID do vendedor desejado aqui

# Consulta SQL para obter o nome do vendedor e as vendas realizadas por ele
sql = """
    SELECT vendedor.nome_vendedor, vendas.id_compra, produtos_venda.referencia, produtos_venda.modelo, produtos_venda.genero, produtos_venda.quantidade, produtos_venda.valor
    FROM vendas
    INNER JOIN vendedor ON vendas.id_vendedor = vendedor.idvendedor
    INNER JOIN produtos_venda ON vendas.id_compra = produtos_venda.id_compra
    WHERE vendas.id_vendedor = %s
"""

# Execução da consulta SQL com o parâmetro do ID do vendedor
cursor.execute(sql, (id_vendedor,))

# Recuperação dos resultados da consulta
resultados = cursor.fetchall()

# Exibição dos resultados
for linha in resultados:
    nome_vendedor = linha[0]
    id_compra = linha[1]
    referencia = linha[2]
    modelo = linha[3]
    genero = linha[4]
    quantidade = linha[5]
    valor = linha[6]

    print(f"Vendedor: {nome_vendedor}")
    print(f"ID da Compra: {id_compra}")
    print(f"Referência: {referencia}")
    print(f"Modelo: {modelo}")
    print(f"Gênero: {genero}")
    print(f"Quantidade: {quantidade}")
    print(f"Valor: {valor}")
    print()

# Fechar o cursor e a conexão com o banco de dados
cursor.close()
conexao.close()
