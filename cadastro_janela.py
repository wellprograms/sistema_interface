from PyQt5 import uic, QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QMessageBox
from classes import *
from decimal import Decimal


class CadastroJanela(QtWidgets.QMainWindow):
    def __init__(self,janela_principal, loja):
        super().__init__()
        uic.loadUi('janela_cadastro.ui', self)
        self.loja = loja
        self.pushButton.clicked.connect(self.cadastrar_produto)
        self.janela_principal = janela_principal

    def cadastrar_produto(self):
        try:
            referencia = int(self.lineEdit.text())
            modelo = self.lineEdit_3.text()
            genero = self.lineEdit_2.text()
            quantidade = int(self.lineEdit_6.text())
            valor = Decimal(str(self.lineEdit_4.text()))
        except:
            QMessageBox.information(self, 'ERRRO', 'DADOS INVALIDOS ')
        try:
            self.loja.estoque.adicionar_produtos(referencia, modelo, genero, quantidade, valor)
            QMessageBox.information(self, 'Cadastro de Produto', 'Produto cadastrado com sucesso.')
        except:
            QMessageBox.information(self, 'ERRRO', 'DADOS INVALIDOS ')
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_6.clear()
        self.close()
        self.loja.estoque.dados_produtos()
        self.janela_principal.abrir_janela_estoque()
        return