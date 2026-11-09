# Contrato do CSV

O upload aceita arquivo `.csv` com até **10 MB** e **10 mil vendas após deduplicação**. Use [vendas_loja.csv](../vendas_loja.csv) como exemplo. O cabeçalho deve conter:

| Coluna | Formato | Regra |
| --- | --- | --- |
| `id_venda` | Identificador | Obrigatório |
| `data` | Data reconhecida pelo pandas | Obrigatória |
| `cliente` | Texto | Obrigatório |
| `cidade` | Texto | Obrigatório |
| `produto` | Texto | Obrigatório |
| `categoria` | Texto | Obrigatória |
| `quantidade` | Número inteiro | Maior que zero |
| `preco_unitario` | Número | Zero ou maior |
| `desconto` | Fração decimal | Entre 0 e 1; `0.15` significa 15% |
| `metodo_pagamento` | Texto | Obrigatório |
| `avaliacao` | Número | Entre 0 e 5; ausências parciais usam a mediana |

O app rejeita uma coluna numérica obrigatória vazia, um desconto fora do intervalo e uma base com todas as avaliações vazias. Linhas repetidas pela combinação `data`, `cliente`, `produto` e `quantidade` são removidas. `valor_liquido = quantidade × preco_unitario × (1 - desconto)`.

Não envie dados reais ao GitHub: o upload é processado em memória. Veja [operação](operations.md) para o ciclo de vida da sessão.
