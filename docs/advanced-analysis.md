# Análises avançadas

A rota `/analises` usa os mesmos filtros do dashboard.

## Clientes RFM

Para cada cliente: recência em dias desde a última compra até o dia seguinte à última venda do recorte, frequência de pedidos e soma do valor líquido. A regra atual classifica como “Cliente VIP” quem tem valor ≥ R$ 4.000 **ou** frequência ≥ 2. “Potencial Lealdade” exige recência ≤ 20 dias e valor ≥ R$ 1.500; os demais ficam em “Regular / Em Risco”. A ordem das regras importa: VIP prevalece.

## Tendência

Regressão linear sobre faturamento diário, com horizonte de 1 a 60 dias. Exige vendas em pelo menos dois dias. A estimativa é exploratória e não representa meta nem previsão garantida.

## Correlação

Matriz de correlação entre quantidade, preço unitário, desconto, avaliação e valor líquido. O gráfico lateral mostra o valor líquido **médio** por categoria para todo o recorte filtrado.

## Exploração 3D

Cruza quantidade, preço unitário e avaliação por categoria. A visualização carrega Plotly apenas nesta seção e mostra até os primeiros 1.000 pontos do recorte; a tabela abaixo apresenta os primeiros 20 desses pontos.
