from classes import *

print ('version == 0000.1')
exit = False
nome_loja = input('Nome e endereço da loja, por favor:').split()

while exit == False:
    loja = Loja(nome_loja[0], nome_loja[1])
    loja.start_sistema()
    opcao = loja.opcao_menu()
    if opcao == 1:
        loja.acao_funcionarios()
    elif opcao == 2:
        loja.acao_estoque()
    elif opcao == 3:
        loja.acao_sistema_caixa()



