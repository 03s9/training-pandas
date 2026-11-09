# Direção visual

A interface usa **bento moderno** para organizar a leitura gerencial e uma landing de portfólio. A escolha foi feita com a skill `ui-ux-pro-max`.

| Papel | Valor |
| --- | --- |
| Fundo | `#f8fafc` |
| Texto e superfícies escuras | `#0f172a` |
| Azul principal | `#2563eb` |
| Azul claro | `#3b82f6` |
| Borda | `#e2e8f0` |
| Títulos | Outfit |
| Corpo e controles | Work Sans |

O dashboard dá prioridade a quatro KPIs e depois à tendência, comparações e tabela. O layout adapta a grade em larguras de 1100, 800 e 560 px. Estados de carregamento, erro e vazio têm mensagens próprias. Controles têm foco visível; animações são removidas com `prefers-reduced-motion`. O gráfico 3D tem tabela complementar e é carregado somente na área avançada.

O CSS fonte está em [web/src/style.css](../web/src/style.css).
