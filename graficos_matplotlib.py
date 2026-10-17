import matplotlib.pyplot as plt
from pandas_dashboard import VendasLoja

fig = plt.figure(figsize=(10, 7))

ax = fig.add_subplot(111, projection='3d')


scatter = ax.scatter(
    VendasLoja['quantidade'],       # Eixo X
    VendasLoja['preco_unitario'],   # Eixo Y
    VendasLoja['avaliacao'],        # Eixo Z (Altura)
    c=VendasLoja['valor_liquido'],  # Cor das bolinhas
    cmap='viridis',
    s=100,                          # Tamanho das bolinhas
    alpha=0.9
)

ax.set_title('Gráfico 3D: Quantidade vs Preço vs Avaliação', fontsize=14, fontweight='bold')
ax.set_xlabel('Quantidade')
ax.set_ylabel('Preço Unitário (R$)')
ax.set_zlabel('Avaliação (Nota)')

plt.colorbar(scatter, label='Valor Líquido (R$)', pad=0.1)
plt.show()