from classes import *

print ('version == 0000.1')
exit = False

loja = Loja("ascona", "vila-sabrina")
loja.start_sistema()
loja.acao_sistema_caixa()
while not exit:
    loja.passar_produto()

