from classes import *

print ('version == 0000.1')
exit = False
nome_loja = input('Nome e endereço da loja, por favor:').split()

loja = Loja(nome_loja[0], nome_loja[1])
loja.start_sistema()
loja.opcao_menu()
exit = False
while exit == False:
    if loja.sistema == True:
        cod = int(input('Digite o codigo do produto: '))
        loja.passar_produto(cod)