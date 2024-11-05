# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

sns.set()

# %%
def plot_pivot_tabela(df, values, index, aggfunc, ylabel, xlabel, opcao='nada'):
    
    if opcao == 'unstack':
        pd.pivot_table(df, values=values, index=index, aggfunc=aggfunc).unstack().plot(figsize=[15, 5])
    elif opcao == 'nada':
        pd.pivot_table(df, values=values, index=index, aggfunc=aggfunc).plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=values, index=index, aggfunc=aggfunc).sort_values(values).plot(figsize=[15, 5])

    
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    
    return None


# %%
print('O nome do nosso script é: ', sys.argv[0])
mes = sys.argv[1]
print(f'Mês de referência é: {mes}')
# %%
sinasc = pd.read_csv('./input/SINASC_RO_2019_'+mes+'.csv')

# %%
max_data = sinasc['DTNASC'].max()[:7]
print(max_data)

# %%
os.makedirs('./output/figs/'+max_data, exist_ok=True)

# %%
plot_pivot_tabela(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'count', 'qtd. por sexo', 'dtnasc', 'unstack')
plt.savefig('./output/figs/'+max_data+'/media_idade_mae_sexo.png')
plt.close()

# %%
plot_pivot_tabela(sinasc, 'APGAR5', 'GESTACAO', 'mean', 'apgar5 medio', 'gestacao', 'sort')
plt.savefig('./output/figs/'+max_data+'/media_apgar5_por_gestacao.png')
plt.close()

# %%
plot_pivot_tabela(sinasc, 'IDADEMAE', 'DTNASC', 'mean', 'qtd. nascimentos', 'data de nascimento')
plt.savefig('./output/figs/'+max_data+'/media_apgar5_por_gestacao.png')
plt.close()


