from classes import *
import pandas as pd

loja = Loja('ascona', 'vila-sabrina')
a = loja.estoque.produtos
df = pd.DataFrame(a)
print(df)