# Guia do dashboard

A rota `/dashboard` mostra a leitura gerencial da base selecionada.

1. **Fonte:** a base de demonstração é carregada automaticamente. Use “Carregar CSV real” para analisar suas vendas.
2. **Filtros:** selecione data inicial, data final, uma cidade e uma categoria. O campo em branco representa todas as cidades ou categorias. “Limpar filtros” volta ao recorte completo.
3. **Indicadores:** faturamento líquido, pedidos, ticket médio por pedido e itens vendidos usam o mesmo recorte.
4. **Gráficos:** evolução diária, faturamento por categoria e por cidade são calculados sobre as vendas filtradas.
5. **Tabela:** as vendas aparecem da data mais recente para a mais antiga, com 20 registros por página.

Se o recorte não tiver vendas, o painel mostra um estado vazio. Se a API falhar, aparece a mensagem de erro e um botão para tentar novamente. O rótulo da fonte distingue demonstração de CSV enviado. A seleção também vale para [análises avançadas](advanced-analysis.md).
