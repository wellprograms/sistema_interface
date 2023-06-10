from PyQt5 import uic, QtCore, QtWidgets, QtGui
from message_boxe import MsgBoxe

from classes import *


class Janela_Caixa(QtWidgets.QMainWindow):
    def __init__(self, janela_principal, loja):
        super().__init__()
        uic.loadUi("janela_caixa.ui", self)
        self.loja = loja
        self.pushButton_2.clicked.connect(self.passar_compras)
        self.pushButton.clicked.connect(self.msg_box)
        

            # Criar o modelo de tabela
        self.table_model = QtGui.QStandardItemModel()
        self.tableView.setModel(self.table_model)

        # Configurar as colunas da tabela
        self.table_model.setColumnCount(5)
        self.table_model.setHorizontalHeaderLabels(["Referência", "Modelo", "Gênero", "Quantidade", "Valor"])
        self.tableView.setColumnWidth(0, 100)  # Definir largura da coluna "Referência" como 100 pixels




    def passar_compras(self):
        verificacao = None
        try:
            cod = int(self.lineEdit.text())
            prod = self.loja.passar_produto(cod)
            if prod == False:
                verificacao = False
            else:
                verificacao = True
        except:
            print('Digite um numero inteiro.')
        
        item_existente = None
        #Verificar se o item ja existe na tabela
        for row in range(self.table_model.rowCount()):
            referencia = self.table_model.item(row, 0).text()

            try:
                if int(referencia) == cod:
                    item_existente = row
            except:
                print('erro na verificacao se o item existe na tabela, talvez na tentativa de converter em inteiro.')
        
        if item_existente is not None:
            #Atualiza a coluna quantidade do item existente
            referencia = self.table_model.item(item_existente, 0)
            quantidade_item = self.table_model.item(item_existente, 3)
            quantidade_atual = int(quantidade_item.text())
            valor_item = self.table_model.item(item_existente, 4)
            valor_atual = Decimal(str(valor_item.text()))
            for c in self.loja.estoque.produtos:
                if c['referencia'] == int(referencia.text()):
                    valor = c['valor'] + valor_atual
                    valor_item.setText(str(valor))
            quantidade_item.setText(str(quantidade_atual + 1))
            label = self.frame.findChild(QtWidgets.QLabel, "label_2")
            label.setText(f"TOTAL: {self.loja.total_compras}")

        else:
            if verificacao == True:
                #adicionar um novo item a tabela.
                if len(self.loja.compras_passadas):
                    ultimo_item = self.loja.compras_passadas[-1]

                    info_formatada = f"    referencia: {ultimo_item['referencia']} modelo: {ultimo_item['modelo']} genero: {ultimo_item['genero']} quantidade: {ultimo_item['quantidade']}"\
                                    f" valor: R${ultimo_item['valor']}"
                    self.label_3.setText(info_formatada)
                    # Criar os itens da tabela com as informações do produto
                    referencia_item = QtGui.QStandardItem(str(ultimo_item["referencia"]))
                    modelo_item = QtGui.QStandardItem(ultimo_item["modelo"])
                    genero_item = QtGui.QStandardItem(ultimo_item["genero"])
                    quantidade_item = QtGui.QStandardItem(str(ultimo_item["quantidade"]))
                    valor_item = QtGui.QStandardItem(str(ultimo_item["valor"]))

                    # Adicionar os itens à tabela
                    row = self.table_model.rowCount()
                    self.table_model.setItem(row, 0, referencia_item)
                    self.table_model.setItem(row, 1, modelo_item)
                    self.table_model.setItem(row, 2, genero_item)
                    self.table_model.setItem(row, 3, quantidade_item)
                    self.table_model.setItem(row, 4, valor_item)
                    label = self.frame.findChild(QtWidgets.QLabel, "label_2")
                    label.setText(f"TOTAL: R${self.loja.total_compras}")

        
    
    def limpar_tabela(self):
        self.table_model.clear()
        self.configurar_colunas_tabela()
        label = self.frame.findChild(QtWidgets.QLabel, "label_2")
        label_2 = self.label_3.setText("")
        label.setText("")
    

    def configurar_colunas_tabela(self):
        self.table_model.setColumnCount(5)
        self.table_model.setHorizontalHeaderLabels(["Referência", "Modelo", "Gênero", "Quantidade", "Valor"])
        self.tableView.setColumnWidth(0, 100)  # Definir largura da coluna "Referência" como 100 pixels


    def msg_box(self):
        if self.tableView.model().rowCount() != 0:
            dialog = MsgBoxe()
            resultado = dialog.exec_()
            if resultado == QtWidgets.QDialog.Accepted:
                codigo_vendedor = dialog.lineEdit.text()
                self.loja.id_vendedor = int(codigo_vendedor)
                a = self.loja.finalizar_compras()
                if a == True:
                    self.limpar_tabela()
        else:
            print('compra NAO finalizada.')

