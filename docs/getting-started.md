# Início rápido

## Requisitos

- Python 3.12
- Node.js 20.19+ e npm
- Duas portas locais livres: 8000 para a API e 5173 para o site

## Instalar

Na raiz do repositório:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-api.txt
npm --prefix web ci
```

Em um ambiente virtual criado com `uv venv`, use `uv pip install --python .venv/bin/python -r requirements-api.txt` no lugar de `pip`.

## Executar

Terminal 1, na raiz:

```sh
.venv/bin/python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

Terminal 2, de qualquer diretório:

```sh
npm --prefix web run dev
```

Abra `http://127.0.0.1:5173`. O Vite envia chamadas `/api` para a porta 8000. A landing aparece em `/`, o painel em `/dashboard` e as análises em `/analises`. A base de demonstração aparece até o upload de um CSV.

Para verificar instalação e build, consulte [testes](testing.md).
