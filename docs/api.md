# API local

A API FastAPI escuta em `127.0.0.1:8000` no fluxo de desenvolvimento. A documentação automática fica em `/docs`.

| Método | Rota | Resultado |
| --- | --- | --- |
| `POST` | `/api/datasets` | Recebe multipart `file` e devolve `dataset_id` e `rows` |
| `GET` | `/api/dashboard/{dataset_id}` | Fonte, opções, KPIs, séries, rankings e página de vendas |
| `GET` | `/api/advanced/{dataset_id}` | Resultado de `rfm`, `forecast`, `correlation` ou `3d` |

`demo` é o identificador da base de demonstração. Os dois endpoints GET aceitam `start` e `end` em ISO (`AAAA-MM-DD`), além de `cities` e `categories` repetíveis. O dashboard aceita `page` a partir de 1, com 20 vendas por página. O endpoint avançado exige `analysis`; `days` vale de 1 a 60 para a regressão.

Erros de upload ou parâmetros retornam `422`; CSV acima dos limites retorna `413`; sessão inexistente ou expirada retorna `404`. Um recorte sem vendas retorna KPIs zerados no dashboard e `{"status":"empty"}` nas análises.
