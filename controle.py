from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from classes import *
from caixa_janela import Janela_Caixa

# 59, 37
loja = Loja('Ascona', 'vila-sabrina')

class JanelaPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("janela_menu.ui", self)
        
        self.pushButton.clicked.connect(self.abrir_janela_funcionarios)
        self.pushButton_2.clicked.connect(self.abrir_janela_estoque)
        self.pushButton_3.clicked.connect(self.abrir_janela_caixa)

        self.janela_caixa = None
        self.janela_funcionarios = None
        self.janela_estoque = None

    def abrir_janela_caixa(self):
        if self.janela_funcionarios:
            self.janela_funcionarios.close()
        if self.janela_estoque:
            self.janela_estoque.close()
        self.hide()
        self.janela_caixa = Janela_Caixa(self, loja)
        self.janela_caixa.show()

    def abrir_janela_funcionarios(self):
        if self.janela_estoque:
            self.janela_estoque.close()
        self.hide()
        self.janela_funcionarios = JanelaFuncionarios(self)
        self.janela_funcionarios.show()

    def abrir_janela_estoque(self):
        if self.janela_funcionarios:
            self.janela_funcionarios.close()
        self.hide()
        self.janela_estoque = JanelaEstoque(self)
        self.janela_estoque.show()


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


class JanelaFuncionarios(QtWidgets.QMainWindow):
    def __init__(self, janela_principal):
        super().__init__()
        uic.loadUi("tabela_menu.ui", self)
        self.pushButton.clicked.connect(janela_principal.abrir_janela_funcionarios)
        self.pushButton_2.clicked.connect(janela_principal.abrir_janela_estoque)
        self.pushButton_3.clicked.connect(janela_principal.abrir_janela_caixa)

        # Aqui você pode acessar os elementos da janela "tabela_menu.ui" normalmente
        # Exemplo: self.treeView, self.pushButton, etc.

        empregados = loja.dados_funcionarios()
        df = pd.DataFrame(empregados)

        model = QStandardItemModel()
        model.setColumnCount(df.shape[1])

        for col in range(df.shape[1]):
            header_item = QStandardItem(df.columns[col])
            model.setHorizontalHeaderItem(col, header_item)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[row, col]))
                model.setItem(row, col, item)

        model.itemChanged.connect(self.dados_alterados)  # Conexão do sinal itemChanged ao slot dados_alterados
        self.treeView.setModel(model)
        self.treeView.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    
    def dados_alterados(self, item):
        # Slot que é chamado quando um item é alterado no modelo
        novo_valor = item.data(Qt.DisplayRole)  # Obtenha o novo valor do item
        print(novo_valor)


class JanelaEstoque(QtWidgets.QMainWindow):
    def __init__(self, janela_principal):
        super().__init__()
        uic.loadUi("tabela_estoque.ui", self)
        self.pushButton.clicked.connect(janela_principal.abrir_janela_funcionarios)
        self.pushButton_2.clicked.connect(janela_principal.abrir_janela_estoque)
        self.pushButton_3.clicked.connect(janela_principal.abrir_janela_caixa)

        # Aqui você pode acessar os elementos da janela "tabela_estoque.ui" normalmente
        # Exemplo: self.treeView, self.pushButton, etc.

        produtos = loja.estoque.produtos
        df = pd.DataFrame(produtos)

        model = QStandardItemModel()
        model.setColumnCount(df.shape[1])

        for col in range(df.shape[1]):
            header_item = QStandardItem(df.columns[col])
            model.setHorizontalHeaderItem(col, header_item)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[row, col]))
                model.setItem(row, col, item)

        self.treeView.setModel(model)
        self.treeView.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)


app = QtWidgets.QApplication([])
janela_principal = JanelaPrincipal()
janela_login = JanelaLogin()
janela_login.show()
app.exec()