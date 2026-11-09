# Problemas comuns

| Sintoma | Causa provável | Ação |
| --- | --- | --- |
| `ENOENT ... /Users/03s9/package.json` | npm executado fora de `web/` | Use `npm --prefix web install` na raiz do repo ou passe o caminho absoluto após `--prefix`. |
| `No module named pip` em `.venv` | Ambiente criado com `uv venv` | Use `uv pip install --python .venv/bin/python -r requirements-api.txt`. |
| `Could not resolve host` | Terminal sem acesso ao registro de pacotes | Verifique rede/DNS no Terminal que instala dependências; o build exige pacotes npm. |
| `EPERM` ao abrir 8000 ou 5173 | Processo em sandbox que bloqueia portas | Inicie os servidores no Terminal local fora do sandbox. |
| Dashboard mostra erro de sessão | API reiniciou ou upload passou de uma hora | Reenvie o CSV. |
| Dashboard sem vendas | Filtros excluíram todas as linhas | Limpe os filtros e ajuste o período. |
| Tendência indisponível | Menos de dois dias com vendas | Amplie o período ou a seleção. |

A API responde erros de CSV inválido ao lado do campo de upload no site. Para diferenças entre o CSV enviado e a base de demonstração, confira o rótulo de fonte no painel.
