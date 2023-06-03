import mysql.connector

# Estabelece a conexão com o banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="well97",
    database="db_sistema")

# Cria um objeto cursor para executar consultas SQL
cursor = conn.cursor()

# Define a instrução SQL para adicionar o registro à tabela funcionarios
add_funcionario_query = """
INSERT INTO funcionarios (nome, funcao, salario, loja_id)
VALUES ('Wellyson', 'Caixa', 1800, 1)
"""

# Executa a instrução SQL para adicionar o registro
cursor.execute(add_funcionario_query)

# Confirma as alterações no banco de dados
conn.commit()

# Fecha o cursor e a conexão
cursor.close()
conn.close()