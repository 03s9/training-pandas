# Handoff
- Active Goal: substituir a UI principal por landing de portfólio e dashboard React, com FastAPI em Python 3.12.
- Branch: feat/gestor-dashboard; commits locais 7ece23b (API) e 23898b9 (validação).
- Touched Files: api.py, pandas_dashboard.py, requirements-api.txt, tests/test_api.py, web/src/, web/package.json, README.md.
- Test/Build Status: 8 testes Python PASS; API demo/upload/filtros/4 análises PASS; TSX parse PASS.
- Blocker: terminal sem DNS para registry.npmjs.org; Recharts, Plotly JS e outros pacotes npm ausentes do cache; npm install/build e revisão visual pendentes.
- Next Exact Action: quando houver rede, executar cd web && npm install && npm run build.
- Next Exact Action: iniciar .venv/bin/python -m uvicorn api:app --reload e npm run dev; revisar em 375/768/1440 px e fluxos de upload, filtros e análises.
- Next Exact Action: corrigir falhas observadas, atualizar testes/documentação e fazer commit local; não fazer push sem ordem.
