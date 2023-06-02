from classes import Loja, Funcionario, OperadorCaixa

loja1 = Loja('ascona', 'vila-sabrina')
loja1.start_sistema()
a = loja1.opcao_menu()
menu = True
while menu:
    if a == 1:
        loja1.acao_funcionarios()
    if a == 2:
        loja1.acao_estoque()
    if a == 3:
        loja1.acao_sistema_caixa()
    else:
        menu = False


