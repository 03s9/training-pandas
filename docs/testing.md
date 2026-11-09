# Testes e verificação

Na raiz do projeto, com o ambiente Python 3.12 instalado:

```sh
.venv/bin/python -m pytest -q
```

A suíte cobre validação do CSV, cálculo do valor líquido, upload, filtros, erros de sessão e estados vazios/insuficientes. Os dois testes legados também entram na coleta.

Build do site:

```sh
npm --prefix web ci
npm --prefix web run build
```

Revisão manual antes de publicar: conferir landing, dashboard e quatro análises; upload válido/inválido; filtros e paginação; estados de erro e vazio; larguras de 375, 768 e 1440 px; navegação por teclado e foco visível. O build não substitui essa revisão visual.

Validação mais recente na branch de desenvolvimento: **8 testes Python passaram** e o build Vite passou. O sandbox usado na implementação bloqueou a abertura das portas locais, então a revisão visual no navegador permanece pendente.
