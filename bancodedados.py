import mysql.connector

# Estabelece a conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="well97",
    database="db_sistema"
)

# Criar tabela "produtos_vendas"
cursor = conexao.cursor()

cursor.execute("""
    ALTER TABLE vendedor DROP COLUMN id_vendedor;
""")


# Fechar a conexão com o banco de dados
conexao.close()