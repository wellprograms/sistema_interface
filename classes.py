import mysql.connector
import pandas as pd
from decimal import Decimal


class Loja:
    conexao = mysql.connector.connect(
    host='localhost',  # Endereço do servidor do banco de dados
    user='root',  # Nome de usuário do banco de dados
    password='well97',  # Senha do banco de dados
    database='loja_bd'  # Nome do banco de dados
    )

    def __init__(self, nome, endereco):
        self.id_compra = 4
        self.nome = nome
        self.endereço = endereco
        self.funcionarios = self.dados_funcionarios()
        self.operadores = self.lista_operadores()
        self.compras_passadas = []
        self.total_compras = Decimal('0')
        self.estoque = Estoque()
        self.sistema = False
        self.operadora = None


    def start_sistema(self):
        print("""       MENU
[01] FUNCIONARIOS
[02] ESTOQUE 
[03] INICIAR SISTEMA DE CAIXA
[04] CONFIGS""")
        print('-='*20)


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


    def acao_estoque(self):
        acao = input('Deseja visualizar/modificar algum produto?')
        if acao == "sim":
            self.estoque.dados_produtos()
            produtos_estoque = self.estoque.produtos
            df = pd.DataFrame(produtos_estoque)
            print(df)
            print()
            acao = int(input('[1] Alterar produto\n[2] Excluir produto\n[3] Adicionar produto\n [4] Voltar ao menu principal.'))
            if acao == 1:
                alteracao = input('Qual produto deseja alterar?')
                for produto in produtos_estoque:
                    if produto['modelo'] == alteracao:
                        acao = int(input(f'Oque deseja alterar no produto {produto["modelo"]}?\n[1] Modelo\n[2] Genero\n[3] Quantidade\n[4] Valor'))
                        if acao == 1:
                            modelo_att = input('digite o modelo atualizado: ')
                            produto['modelo'] = modelo_att
                            self.estoque.alterar_produtos("modelo", alteracao, modelo_att)
                            print('modelo atualizado')
                            self.acao_estoque()
                            return
                        elif acao == 2:
                            genero_att = input('Digite o Genero atualizado: ')
                            produto['genero'] = genero_att
                            self.estoque.alterar_produtos("genero", alteracao, genero_att)
                            print('Genero atualizado.')
                            self.acao_estoque()
                            return
                        elif acao == 3:
                            quantidade_att = int(input('Digite a quantidade atualizada: '))
                            produto['quantidade'] = quantidade_att
                            self.estoque.alterar_produtos("quantidade", alteracao, quantidade_att)                            
                            print('Quantidade atualizada')
                            self.acao_estoque()
                            return
                        elif acao == 4:
                            valor_att = float(input('Digite o valor atualizado.'))
                            produto['valor'] = valor_att
                            self.estoque.alterar_produtos("valor", alteracao, valor_att)
                            print('Valor atualizado')
                            self.acao_estoque()
                            return
            elif acao == 2:
                excluir = input('Qual produto deseja excluir?')
                self.estoque.excluir_produtos(excluir)
                self.acao_estoque()
                pass

            elif acao == 3:
                self.estoque.adicionar_produtos()
                self.acao_estoque()

            elif acao == 4:
                self.start_sistema()
                self.opcao_menu()


    def acao_funcionarios(self):
        acao = input('Deseja visualizar/modificar algum funcionario?')
        if acao == "sim":
            membros = self.dados_funcionarios()
            df = pd.DataFrame(membros)
            print(df)
            print()
            acao = int(input('[1] Alterar funcionario\n[2] Adicionar funcionario\n[3] Retornar ao menu anterior'))
            if acao == 1:
                alteracao = input('Qual funcionario deseja alterar?')
                for funcionario in membros:
                    if funcionario['nome'] == alteracao:
                        acao = int(input(f'Oque deseja alterar no funcionario {funcionario["nome"]}?\n[01]Nome\n[02]Salario\n[03]Função'))
                        if acao == 1:
                            nome_att = input('Digite o nome atualizado.')
                            funcionario['nome'] = nome_att
                            print('nome atualizado')
                            self.gerenciar_funcionarios("nome",alteracao, nome_att)
                            print('Alteracao realizada com sucesso.')
                            self.acao_funcionarios()
                            return
                        
                        elif acao == 2:
                            salario_att = float(input('Digite o salário atualizado'))
                            funcionario['salario'] = salario_att
                            print('salario atualizado')
                            self.gerenciar_funcionarios("salario",alteracao, salario_att)
                            return
                        
                        elif acao == 3:
                            funcao_att = input('Digite a funcao atualizada: ')
                            funcionario['funcao'] = funcao_att
                            print('Funcao atuaizada')
                            self.gerenciar_funcionarios("funcao", alteracao, funcao_att)
                            return
                        

            elif acao == 2:
                nome = input('Nome funcionario: ')
                funcao = input('Funcao funcionario')
                self.adicionar_funcionario(Funcionario(nome, funcao))
                self.acao_funcionarios()
            elif acao == 3:
                self.start_sistema()
                self.opcao_menu()
        

    def acao_sistema_caixa(self):
        print('Faça login para iniciar o sistema.')
        nome = input('nome: ')
        login = input('login: ')
        senha = input('senha: ')
        for operador in self.operadores:
            if nome == operador['nome'] and login == operador['login'] and senha == operador['senha']:
                self.operadora = OperadorCaixa(operador['id_operador'],operador['nome'], operador['login'], operador['senha'])
        print(f"Sistema iniciado com sucesso. Operadora: {self.operadora.nome}")
        self.sistema = True
        return
    

    def pegar_idcompra(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT MAX(id_compra) FROM vendas")
        resultado = cursor.fetchone()
        id_compra_atual = resultado[0]

        # Verificar se o resultado é None (ou seja, a tabela está vazia)
        if id_compra_atual is None:
            id_compra_atual = 0

        return id_compra_atual + 1


    def passar_produto(self, cod):
        cursor = self.conexao.cursor()
        id_compra = self.pegar_idcompra()
        if cod == 000:
            codigo_vendedor = int(input('Digite o COD do Vendedor'))
            print(f'Compra finalizada. Valor total: {self.total_compras}')
            id_operador = self.operadora.id_operador
            id_vendedor = codigo_vendedor
            cursor.execute("INSERT INTO vendas (id_compra, id_operador, id_vendedor) VALUES (%s, %s, %s)",
               (id_compra, id_operador, id_vendedor))
            for produto in self.compras_passadas:
                referencia = produto['referencia']
                modelo = produto['modelo']
                genero = produto['genero']
                quantidade = produto['quantidade']
                valor = produto['valor']

                # Executar a consulta de inserção na tabela 'produtos_venda'
                cursor.execute("INSERT INTO produtos_venda (id_compra, referencia, modelo, genero, quantidade, valor) "
                            "VALUES (%s, %s, %s, %s, %s, %s)",
                            (id_compra, referencia, modelo, genero, quantidade, valor))
                self.conexao.commit()
            self.compras_passadas.clear()
            
            acao = int(input("[1] Nova compra - [2] Finalizar sistema - [3]Menu inicial"))
            if acao == 1:
                cod = int(input('Codigo produto: '))
                return self.passar_produto(cod)
            if acao == 2:
                return 2
            if acao == 3:
                self.start_sistema()
                self.opcao_menu()

        produto_encontrado = False

        for produto in self.estoque.produtos:
            if cod == produto['referencia']:
                self.total_compras += Decimal(str(produto['valor']))
                self.compras_passadas.append(produto)
                produto_encontrado = True
                continue

        if not produto_encontrado:
            print('Produto inexistente. Tente novamente')
        print(self.total_compras)


    def inserir_dados_loja(self):
        cursor = Loja.conexao.cursor()
        sql = f'INSERT INTO loja_dados(nome_loja, end_loja) VALUES ("{self.nome}", "{self.endereço}")'
        cursor.execute(sql)
        Loja.conexao.commit()
        return

    
    def adicionar_funcionario(self, funcionario):
        cursor = Loja.conexao.cursor()
        if funcionario.funcao == 'Caixa':
            id_cadastro = int(input('ID_OPERADOR: '))
            login_cadastro = input('login: ')
            senha_cadastro = input('senha: ')
            cadastro_oc = OperadorCaixa(id_cadastro, funcionario.nome, login_cadastro, senha_cadastro)
            saql = f'INSERT INTO operador_caixa(id_operador, nome, login, senha) VALUES ({cadastro_oc.id_operador}, "{cadastro_oc.nome}", "{cadastro_oc.login}", "{cadastro_oc.senha}")'
            cursor.execute(saql)
            print('Cadastro realizado com sucesso.')
        sql = f'INSERT INTO funcionarios(nome, funcao, salario) VALUES ("{funcionario.nome}", "{funcionario.funcao}", {funcionario.salario})'
        cursor.execute(sql)
        Loja.conexao.commit()
        print('Cadastro realizado com sucesso.')
        self.acao_funcionarios()


    
    def gerenciar_funcionarios(self, coluna, atual, novo):
        cursor = Loja.conexao.cursor()
        sql = f"UPDATE funcionarios SET {coluna} = %s WHERE nome = %s"
        cursor.execute(sql, (novo, atual))
        Loja.conexao.commit()
        return


    def dados_funcionarios(self):
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
        cursor = Loja.conexao.cursor()
        sql = "SELECT id_operador, nome, login, senha FROM operador_caixa"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        lista_dici = []
        dici_dados = {}
        for linha in resultado:
            dici_dados['id_operador'] = linha[0]
            dici_dados['nome'] = linha[1]
            dici_dados['login'] = linha[2]
            dici_dados['senha'] = linha[3]
            lista_dici.append(dici_dados.copy())
        return lista_dici


class Funcionario:
    def __init__(self, nome, funcao):
        self.salario = 1800.00
        self.nome = nome
        self.funcao = funcao 
        self.vendas = []

    def venda(self, valor):
        self.vendas.append(valor)
    

class Estoque(Loja):
    def __init__(self):
        self.produtos = self.dados_produtos()
    
    def dados_produtos(self):
        print('-='*30)
        cursor = Loja.conexao.cursor()
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
        return lista_dici


    def adicionar_produtos(self):
        referencia = int(input('referencia: '))
        modelo = input('modelo: ')
        genero = input('genero: ')
        quantidade = int(input('quantidade: '))
        valor = float(input('valor: '))
        valores = (referencia, modelo, genero, quantidade, valor)
        cursor = self.conexao.cursor()
        sql = 'INSERT INTO produtos(referencia, modelo, genero, quantidade, valor) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql, valores)
        Loja.conexao.commit()
        return

    def alterar_produtos(self, coluna, atual, novo):
        cursor = self.conexao.cursor()
        sql = f"UPDATE produtos SET {coluna} = %s WHERE modelo = %s"
        cursor.execute(sql, (novo, atual))
        Loja.conexao.commit()
        return
    
    def excluir_produtos(self, produto):
        cursor = self.conexao.cursor()
        sql = f"DELETE FROM produtos WHERE referencia = %s"
        valor = produto
        cursor.execute(sql, (valor,))
        self.conexao.commit()
        return
    

class OperadorCaixa(Loja):
    def __init__(self,id_operador, nome, login, senha):
        self.produtos_passados = []
        #cursor = Loja.conexao.cursor()
        self.nome = nome
        self.login = login
        self.senha = senha
        self.id_operador = id_operador
        #sql = f'INSERT INTO operador_caixa (id_operador, nome, login, senha) VALUES ({self.id_operador},"{self.nome}", "{self.login}", "{self.senha}")'
        #cursor.execute(sql)
        #Loja.conexao.commit()


class Vendedor(Loja):
    def __init__(self, id_vendedor, nome_vendedor):
        self.id_vendedor = id_vendedor
        self.nome_vendedor = nome_vendedor
        cursor = Loja.conexao.cursor()
        sql = f'INSERT INTO vendedor (id_vendedor, nome_vendedor) VALUES ({self.id_vendedor},"{self.nome_vendedor}")'
        cursor.execute(sql)
        Loja.conexao.commit()

