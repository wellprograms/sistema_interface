from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from classes import *
from decimal import Decimal

class AtualizarJanela(QtWidgets.QMainWindow):
    def __init__(self, janela_principal, loja):
        super().__init__()
        uic.loadUi("atualizar_janela.ui", self)
        self.loja = loja
        self.pushButton.clicked.connect(self.atualizar_produtos)
        self.janela_principal = janela_principal
    

    def atualizar_produtos(self):
        try:
            referencia = int(self.lineEdit.text())
            modelo = self.lineEdit_2.text() 
            genero = self.lineEdit_3.text()
            quantidade = int(self.lineEdit_4.text())
            valor = Decimal(str(self.lineEdit_5.text()))
            self.loja.estoque.alterar_produtos(referencia, modelo, genero, quantidade, valor)
            QMessageBox.information(self, f"{referencia}",  "atualizado com sucesso.")
            self.loja.estoque.dados_produtos()
            self.janela_principal.abrir_janela_estoque()

        except:
            QMessageBox.information(self, "Erro!",  f"O produto {referencia} não pode ser atualizado.")
        self.close()


