from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

from classes import *
import pandas as pd

loja = Loja('Ascona', 'vila-sabrina')

class JanelaLogin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("janela_login.ui", self)
        self.pushButton.clicked.connect(self.fazer_login)

        self.setTabOrder(self.lineEdit_2, self.lineEdit_3)
        self.setTabOrder(self.lineEdit_3, self.pushButton)

        self.lineEdit_3.returnPressed.connect(self.fazer_login)

    def fazer_login(self):
        usuario = self.lineEdit_2.text()
        senha = self.lineEdit_3.text()
        if loja.start_sistema(usuario, senha):
            self.close()
            janela_principal.show()

    def keyPressEvent(self, event):
        # Verificar se a tecla pressionada é a tecla Enter
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            # Executar ação desejada, como chamar fazer_login
            self.fazer_login()


class JanelaMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("janela_menu.ui", self)
        self.pushButton.clicked.connect(self.funcionarios)
        self.pushButton_2.clicked.connect(self.estoque)

    def funcionarios(self):
        self.close()
        janela_opcao.show()

    def estoque(self):
        self.close()
        janela_estoque.show()


class JanelaEstoque(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("tabela_estoque.ui", self)
        produtos = loja.estoque.produtos
        df=pd.DataFrame(produtos)

        # Criar o modelo de item
        model = QStandardItemModel()
        model.setColumnCount(df.shape[1])

        # Preencher o modelo com os nomes das colunas
        for col in range(df.shape[1]):
            header_item = QStandardItem(df.columns[col])
            model.setHorizontalHeaderItem(col, header_item)

        # Preencher o modelo com os valores das linhas
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[row, col]))
                model.setItem(row, col, item)
        
        self.treeView.setModel(model)
        # Ajustar o tamanho das colunas automaticamente
        self.treeView.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    

class JanelaFuncionarios(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("tabela_menu.ui", self)
        empregados = loja.dados_funcionarios()
        df = pd.DataFrame(empregados)

        # Criar o modelo de item
        model = QStandardItemModel()
        model.setColumnCount(df.shape[1])

        # Preencher o modelo com os nomes das colunas
        for col in range(df.shape[1]):
            header_item = QStandardItem(df.columns[col])
            model.setHorizontalHeaderItem(col, header_item)

        # Preencher o modelo com os valores das linhas
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[row, col]))
                model.setItem(row, col, item)
        
        self.treeView.setModel(model)
        # Ajustar o tamanho das colunas automaticamente
        self.treeView.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    


app = QtWidgets.QApplication([])
janela_estoque = JanelaEstoque()
janela_opcao = JanelaFuncionarios()
janela_principal = JanelaMenu()  # Criar instância da janela principal
formulario = JanelaLogin()
formulario.show()
app.exec()
