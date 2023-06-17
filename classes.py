import mysql.connector
import pandas as pd
from decimal import Decimal


class Loja:
    # Init
    # param nome : recebe nome da loja
    # param endereco : recebe endereco da loja
    conexao = mysql.connector.connect(
    host='localhost',  # Endereço do servidor do banco de dados
    user='root',  # Nome de usuário do banco de dados
    password='Wellyson-0',  # Senha do banco de dados
    database='db_sistema'  # Nome do banco de dados
    )
    # Atributos:
    def __init__(self, nome, endereco):
        self.id_compra = 4
        self.id_vendedor = 0
        self.nome = nome
        self.endereço = endereco
        self.funcionarios = self.dados_funcionarios()
        self.operadores = self.lista_operadores()
        self.compras_passadas = []
        self.total_compras = Decimal('0')
        self.estoque = Estoque()
        self.sistema = False
        self.operadora = None

    # Funcao inicial exibe o menu do sistema
    def start_sistema(self, login, senha):
        print('Faça login para iniciar o sistema.')
        nome = "Wellyson"
        login = login
        senha = senha
        for operador in self.operadores:
            if nome == operador['nome'] and login == operador['login'] and senha == operador['senha']:
                self.operadora = OperadorCaixa(operador['id_operador'],operador['nome'], operador['login'], operador['senha'])
                print(f"Sistema iniciado com sucesso. Operadora: {self.operadora.nome}")
                self.sistema = True
                return True
            else:
                print('Username or password incorrect')


    """ Método pede para que o usuario escolha 1 opcao das apresentadas no método start_sistema
    e chama outro método da instancia baseado na escolha do usuário"""
    def opcao_menu(self):
        opcao = int(input('Sua opcão: '))
        if opcao == 1:
            if len(self.funcionarios) < 1:
                print(f'Nosso quadro de funcionarios está vazio, nenhum funcionario foi contratado pela {self.nome}')
            else:
                print(f'Temos {len(self.funcionarios)} funcionarios contratado no momento.')
                self.acao_funcionarios()
        elif opcao == 2:
            self.acao_estoque()
        elif opcao == 3:
            self.acao_sistema_caixa()
        else:
            return                        
        

    """Método é basicamente um login, onde o usuário preenche as informacoes, e o método verifica atraves do atributo da instancia operadores
    que recebe o metodo lista_operadores, se os dados inseridos forem correspondentes, o método atribui ao atributo operadora uma instancia da class
    OperadorCaixa, altera o atributo sistema para True, e retorna que o sistema foi iniciado"""

    def acao_sistema_caixa(self, login, senha):
        # Método para iniciar o sistema de caixa através do login feito pelo usuário, se tiver permissao de operador de caixa ou adm, inicia.
        # O self.operadora passa a receber uma instancia do objeto OperadorCaixa.
        print('Faça login para iniciar o sistema.')
        nome = "Wellyson"
        login = login
        senha = senha
        """Percorre a lista de operadores que existe no banco de dados e compara com o login que o usuario inseriu
        se igual, o sistema do caixa passa a ser True e habilitado para o método passar_produto."""
        for operador in self.operadores:
            if nome == operador['nome'] and login == operador['login'] and senha == operador['senha']:
                self.operadora = OperadorCaixa(operador['id_operador'],operador['nome'], operador['login'], operador['senha'])
                print(f"Sistema iniciado com sucesso. Operadora: {self.operadora.nome}")
                self.sistema = True
                #self.passar_produto()
                break
            else:
                print('Username or password incorrect')
                self.acao_sistema_caixa()
                

    def pegar_idcompra(self):
        """Pega o ultimo id_compra que existe na tabela dentro do banco de dados e retorna ele + 1."""
        cursor = self.conexao.cursor()
        cursor.execute("SELECT MAX(id_compra) FROM vendas")
        resultado = cursor.fetchone()
        id_compra_atual = resultado[0]

        # Verificar se o resultado é None (ou seja, a tabela está vazia)
        if id_compra_atual is None:
            id_compra_atual = 0

        return id_compra_atual + 1


    def passar_produto(self, cod):
        """Verifica se o sistema está habilitado para esse método, em seguida percorre a lista de compras passadas e compara se o produto passado
        ja existe nessa lista, se ja existir , o produto recebe +1 na quantidade, e soma o valor ao atributo total_compras, alem disso, tambem
        transforma a variavel produto_encontrado em True, se o produto for inexistente, tanto na lista de compras passadas, quanto na tabela
        existente no banco de dados, o método retorna False"""

        if not self.sistema:
            print('ERRO! Login nao efetuado.')
            return
        
        produto_encontrado = False

        for produto in self.compras_passadas:
            if cod == produto['referencia']:
                produto['quantidade'] += 1
                self.total_compras += Decimal(str(produto['valor']))
                produto_encontrado = True
                break
        
        # Percorre a tabela produtos do banco de dados atrás do produto passado.
        if not produto_encontrado:
            for produto in self.estoque.produtos:
                if cod == produto['referencia']:
                    self.total_compras += Decimal(str(produto['valor']))
                    produto['quantidade'] = 1
                    self.compras_passadas.append(produto.copy())
                    produto_encontrado = True
                    break # Break para sair do loop logo após encontrar o produto 
            

        if not produto_encontrado:
            print('Produto inexistente. Tente novamente')
            return False

        print(self.total_compras)

    
    def finalizar_compras(self):

        """Método inseri na tabela vendas, o id_compra, id_operador, e id_vendedor ja obtidos em métodos anteriors
        em seguida, o método adiciona produto por produto na tabela produtos_venda do banco de dados, o método tambem
        é encarregado da limpeza dos atributos, retornando aos valores iniciais da instancia
        Método retorna um erro relacionado ao banco de dados, valores passados errados."""
        cursor = self.conexao.cursor()
        id_compra = self.pegar_idcompra()
        operador_id = self.operadora.id_operador
        id_vendedor = self.id_vendedor

        try:
            # Inserir a venda na tabela 'vendas'
            cursor.execute("INSERT INTO vendas (id_compra, id_operador, id_vendedor) VALUES (%s, %s, %s)",
            (id_compra, operador_id, id_vendedor))
            
            self.conexao.commit()

            for produto in self.compras_passadas: 
                referencia = produto['referencia']
                modelo = produto['modelo']
                genero = produto['genero']
                quantidade = produto['quantidade']
                valor = produto['valor'] * produto['quantidade']
                cursor.execute("INSERT INTO produtos_venda (id_compra, referencia, modelo, genero, quantidade, valor) "
                            "VALUES (%s, %s, %s, %s, %s, %s)",
                            (id_compra, referencia, modelo, genero, quantidade, valor))
                self.conexao.commit()
                cursor.execute(self.estoque.diminuir_quantidade(produto['referencia'], 1))
                self.conexao.commit()   

            self.compras_passadas.clear()
            self.total_compras = 0

            return True

        except Exception as erro:
            print(f'Erro ao inserir produtos no banco de dados.{erro}')
            return False
            # Executar a consulta de inserção na tabela 'produtos_venda'


    def inserir_dados_loja(self):
        """Método de insersão de dados sobre a loja no banco de dados ."""
        cursor = Loja.conexao.cursor()
        sql = f'INSERT INTO loja_dados(nome_loja, end_loja) VALUES ("{self.nome}", "{self.endereço}")'
        cursor.execute(sql)
        Loja.conexao.commit()
        return

    
    def adicionar_funcionario(self, funcionario):
        funcionario_id = funcionario.add_funcionario()
        if funcionario.funcao == 'Caixa':
            login_cadastro = input('O funcionario é um OperadorDeCaixa, cadastre um login :')
            senha_cadastro = input('Agora, uma senha: ')
            funcionario.add_operador_caixa(login_cadastro, senha_cadastro, funcionario_id)
        

    def gerenciar_funcionarios(self, coluna, atual, novo):
        """Método utilizado pra alterar informacoes dos funcionarios ja cadastrados no banco de dados."""
        cursor = Loja.conexao.cursor()
        sql = f"UPDATE funcionarios SET {coluna} = %s WHERE nome = %s"
        cursor.execute(sql, (novo, atual))
        Loja.conexao.commit()
        return


    def dados_funcionarios(self):
        """Método retorna uma lista de todos os funcionarios(nome,funcao,salario) cadastrado na tabela no banco de dados."""
        print('-='*30)
        cursor = Loja.conexao.cursor()
        sql = "SELECT nome, funcao, salario FROM funcionarios"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        lista_dici = []
        dici_dados = {}
        for linha in resultado:
            dici_dados['nome'] = linha[0]
            dici_dados['funcao'] = linha[1]
            dici_dados['salario'] = linha[2]
            lista_dici.append(dici_dados.copy())
        return lista_dici
    

    def lista_operadores(self):
        cursor = self.conexao.cursor()
        sql = "SELECT nome, login, senha, id_operador FROM operador_caixa"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        lista_dici = []
        dici_dados = {}
        for linha in resultado:
            dici_dados['nome'] = linha[0]
            dici_dados['login'] = linha[1]
            dici_dados['senha'] = linha[2]
            dici_dados['id_operador'] = linha[3]
            lista_dici.append(dici_dados.copy())
        return lista_dici


class Funcionario(Loja):
    """Método utilizado para facilitar a inserção e manipulação da tabela funcionarios do Banco De Dados.
    recebe como parametros:
    :nome
    :funcao
    :salario
    :loja id"""
    def __init__(self, nome, funcao, salario, loja_id):
        self.salario = salario
        self.nome = nome
        self.funcao = funcao 
        self.loja_id = loja_id

    def add_funcionario(self):
        """Método adiciona um funcionario novo na tabela do Banco de dados. Método utiliza os atributos da instancia ja cadastrados
        método também retorna o funcionario_id"""
        cursor = self.conexao.cursor()
        add_funcionario_query = """
    INSERT INTO funcionarios (nome, funcao, salario, loja_id)
    VALUES (%s, %s, %s, %s)
    """
        cursor.execute(add_funcionario_query, (self.nome, self.funcao, self.salario, self.loja_id))
        funcionario_id = cursor.lastrowid  # Obtém o ID do funcionário inserido
        self.conexao.commit()
        return funcionario_id
    
    def add_operador_caixa(self, login, senha, funcionario_id):
        """Método verifica a funcao do funcionario ja instanciado
        se a funcao for de caixa, método insere em uma tabela específica de operadora
        de caixa além de continuar existindo na tabela funcionarios"""
        if self.funcao == "Caixa":
            cursor = self.conexao.cursor()
            add_operador_caixa_query = """
            INSERT INTO operador_caixa (nome, login, senha, id_operador)
            VALUES (%s, %s, %s, %s)
            """
            values = (self.nome, login, senha, funcionario_id)
            cursor.execute(add_operador_caixa_query, values)
            self.conexao.commit()
            print("Operador de caixa adicionado com sucesso.")
        else:
            print("A função do funcionário não é Caixa. Não é possível adicionar como operador de caixa.")
     
    
class Estoque(Loja):
    """Gerenciamento do estoque dentro do banco de dados. 
    Método oferece recursos pra adicionar, remover, alterar produtos dentro do banco de dados."""
    def __init__(self):
        self.produtos = []
        self.dados_produtos()

    
    def dados_produtos(self):
        """Método retorna uma lista de produtos ja cadastrados no banco de dados"""
        print('-='*30)
        cursor = self.conexao.cursor()
        sql = "SELECT referencia, modelo, genero, quantidade, valor FROM produtos"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        lista_dici = []
        dici_dados = {}
        for linha in resultado:
            dici_dados['referencia'] = linha[0]
            dici_dados['modelo'] = linha[1]
            dici_dados['genero'] = linha[2]
            dici_dados['quantidade'] = linha[3]
            dici_dados['valor'] = linha[4]
            lista_dici.append(dici_dados.copy())
        self.produtos = lista_dici


    def adicionar_produtos(self,referencia,modelo,genero,quantidade,valor):
        """Método adiciona produto ao banco de dados."""
        valores = (referencia, modelo, genero, quantidade, valor)
        cursor = self.conexao.cursor()
        sql = 'INSERT INTO produtos(referencia, modelo, genero, quantidade, valor) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql, valores)
        self.conexao.commit()
        return

    def alterar_produtos(self, referencia, valor1, valor2, valor3, valor4):
        """Método altera produtos dentro do banco de dados."""
        cursor = self.conexao.cursor()
        
        try:
            # Monta a query de atualização para as colunas desejadas
            sql = "UPDATE produtos SET modelo = %s, genero = %s, quantidade = %s, valor = %s WHERE referencia = %s"
            cursor.execute(sql, (valor1, valor2, valor3, valor4, referencia))

            self.conexao.commit()
        except Exception as erro:
            print(erro)
        return


    
    def excluir_produtos(self, produto):
        """Método exclui produtos dentro do banco de dados"""
        cursor = self.conexao.cursor()
        sql = f"DELETE FROM produtos WHERE referencia = %s"
        valor = produto
        cursor.execute(sql, (valor,))
        self.conexao.commit()
        return

    def diminuir_quantidade(self, referencia, quantidade):
        """Método diminui quantidade de produto determinado pelo usuário dentro do banco de dados."""
        cursor = self.conexao.cursor()
        sql = f"UPDATE produtos SET quantidade = quantidade - {quantidade} WHERE referencia = {referencia}"
        cursor.execute(sql)
        self.conexao.commit()

    
class OperadorCaixa(Loja):
    """Classe criada com o intuito de facilitar a manipulacao dentro do banco de dados"""
    def __init__(self, id_operador, nome, login, senha):
        self.produtos_passados = []
        self.nome = nome
        self.login = login
        self.senha = senha
        self.id_operador = id_operador


class Vendedor(Loja):
    def __init__(self, nome_vendedor):
        self.nome_vendedor = nome_vendedor
        #cursor = Loja.conexao.cursor()
        #sql = f'INSERT INTO vendedor (nome_vendedor) VALUES ("{self.nome_vendedor}")'
        #cursor.execute(sql)
        #self.conexao.commit()
    
    def visualizar_vendas(self, id_vendedor):

        # Criar cursor para executar as consultas
        cursor = self.conexao.cursor()

        # ID do vendedor para realizar a consulta
        id_vendedor = id_vendedor  # Insira o ID do vendedor desejado aqui

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

