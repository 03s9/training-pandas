import matplotlib.pyplot as plt
import seaborn as sns

# Conectando com o seu outro arquivo e puxando o DataFrame já tratado!
from pandas_dashboard import VendasLoja

# Configurando o visual do Dashboard (grade 2x2 = 4 gráficos na mesma tela)
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Dashboard de Análise de Vendas', fontsize=18, fontweight='bold')

# 1. Faturamento Líquido por Categoria (Barras)
faturamento_cat = VendasLoja.groupby('categoria')['valor_liquido'].sum().sort_values(ascending=False).reset_index()
sns.barplot(
    data=faturamento_cat,
    x='categoria',
    y='valor_liquido',
    hue='categoria',
    palette='viridis',
    ax=axes[0, 0]
)
axes[0, 0].set_title('1. Faturamento Líquido por Categoria (R$)')
axes[0, 0].set_xlabel('Categoria')
axes[0, 0].set_ylabel('R$')

# 2. Distribuição por Método de Pagamento (Pizza)
pagamentos = VendasLoja['metodo_pagamento'].value_counts()
axes[0, 1].pie(
    pagamentos,
    labels=pagamentos.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=sns.color_palette('pastel')
)
axes[0, 1].set_title('2. Vendas por Método de Pagamento')

# 3. Faturamento por Cidade (Barras Horizontais)
faturamento_cidade = VendasLoja.groupby('cidade')['valor_liquido'].sum().sort_values(ascending=True).reset_index()
sns.barplot(
    data=faturamento_cidade,
    x='valor_liquido',
    y='cidade',
    hue='cidade',
    palette='magma',
    ax=axes[1, 0]
)
axes[1, 0].set_title('3. Faturamento por Cidade (R$)')
axes[1, 0].set_xlabel('Valor Líquido (R$)')
axes[1, 0].set_ylabel('Cidade')

# 4. Evolução das Vendas ao Longo do Tempo (Linha)
vendas_tempo = VendasLoja.groupby('data')['valor_liquido'].sum().reset_index()
sns.lineplot(
    data=vendas_tempo,
    x='data',
    y='valor_liquido',
    marker='o',
    color='royalblue',
    linewidth=2,
    ax=axes[1, 1]
)
axes[1, 1].set_title('4. Evolução Diária do Faturamento')
axes[1, 1].set_xlabel('Data')
axes[1, 1].set_ylabel('Valor Líquido (R$)')
axes[1, 1].tick_params(axis='x', rotation=45)

# Ajusta o layout, salva a imagem do dashboard e abre na tela
plt.tight_layout()
plt.savefig('dashboard_vendas.png', dpi=300)
print("\nDashboard salvo em 'dashboard_vendas.png' e abrindo na tela...")
plt.show()