import pandas as pd
import matplotlib.pyplot as plt

caminho = r'separado.xlsx'
df = pd.read_excel(caminho, sheet_name='Planilha1')

df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y')

df_2018 = df[df['Data'].dt.year == 2018].copy()

df_2018.loc[:, 'Mês'] = df_2018['Data'].dt.month

plt.figure(figsize=(12, 6))
df_2018.boxplot(column='Último', by='Mês', grid=False, showfliers=False)

plt.title('Distribuição do valor do dólar por mês em 2018', fontsize=14)
plt.suptitle('')
plt.xlabel('Mês')
plt.ylabel('Valor do Dólar (Último)')
plt.xticks(rotation=0)
plt.show()

#    O ano de 2018 foi marcado por uma evolução do valor do dólar com períodos de alta volatilidade e
# uma leve tendência de aumento nos valores médios de fechamento. A análise visual dos boxplots revela
# momentos de maior instabilidade (setembro e novembro) e outros de maior estabilidade (abril e outubro).
