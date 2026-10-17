import matplotlib.pyplot as plt
import seaborn as sns
from pandas_dashboard import VendasLoja, RFM_Clientes, TendenciaVendas

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Dashboard Completo de Vendas, Estatística, RFM e Regressão', fontsize=18, fontweight='bold')

# 1. Faturamento por Categoria
faturamento_cat = VendasLoja.groupby('categoria')['valor_liquido'].sum().sort_values(ascending=False).reset_index()
sns.barplot(data=faturamento_cat, x='categoria', y='valor_liquido', hue='categoria', palette='viridis', ax=axes[0, 0])
axes[0, 0].set_title('1. Faturamento por Categoria (R$)')
axes[0, 0].set_xlabel('Categoria')
axes[0, 0].set_ylabel('R$')

# 2. Mapa de Calor de Correlação (Heatmap)
colunas_num = ['quantidade', 'preco_unitario', 'desconto', 'avaliacao', 'valor_liquido']
correlacao = VendasLoja[colunas_num].corr()
sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=axes[0, 1])
axes[0, 1].set_title('2. Mapa de Calor de Correlação')

# 3. Boxplot de Preços e Valores por Categoria
sns.boxplot(data=VendasLoja, x='categoria', y='valor_liquido', hue='categoria', palette='Set2', ax=axes[0, 2])
axes[0, 2].set_title('3. Distribuição e Outliers (Boxplot)')
axes[0, 2].set_xlabel('Categoria')
axes[0, 2].set_ylabel('Valor Líquido (R$)')

# 4. Segmentação RFM de Clientes
segmentos_rfm = RFM_Clientes['segmento'].value_counts().reset_index()
sns.barplot(data=segmentos_rfm, x='segmento', y='count', hue='segmento', palette='magma', ax=axes[1, 0])
axes[1, 0].set_title('4. Clientes por Segmento RFM')
axes[1, 0].set_xlabel('Segmento')
axes[1, 0].set_ylabel('Qtd Clientes')

# 5. Regressão Linear: Evolução + Linha de Tendência
sns.scatterplot(data=TendenciaVendas, x='data', y='valor_liquido', s=80, color='royalblue', label='Real', ax=axes[1, 1])
sns.lineplot(data=TendenciaVendas, x='data', y='tendencia_prevista', color='crimson', linewidth=2.5, label='Regressão Linear', ax=axes[1, 1])
axes[1, 1].set_title('5. Faturamento Diário e Regressão Linear')
axes[1, 1].set_xlabel('Data')
axes[1, 1].set_ylabel('R$')
axes[1, 1].tick_params(axis='x', rotation=35)

# 6. Participação por Método de Pagamento
pagamentos = VendasLoja['metodo_pagamento'].value_counts()
axes[1, 2].pie(pagamentos, labels=pagamentos.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
axes[1, 2].set_title('6. Métodos de Pagamento')

plt.tight_layout()
plt.savefig('dashboard_vendas.png', dpi=300)
print("Dashboard atualizado salvo em 'dashboard_vendas.png'!")
plt.show()