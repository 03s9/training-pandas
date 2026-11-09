# REPO_MAP.md — Mapa Neural de Símbolos e Conexões

> Atualizado em: `2026-11-08 22:13:56`
> **Instrução para IAs (Antigravity, Cursor, Codex)**: Use os intervalos `[L<inicio>-L<fim>]` abaixo para ler apenas as linhas necessárias (`StartLine`/`EndLine`). Nunca leia arquivos inteiros grandes sem consultar este mapa.

**Resumo do Grafo**: `7` arquivos indexados | `13` símbolos mapeados.

### `app_streamlit.py` (Python, 158 lines)
  - `def moeda()` [L22-L23]
  - `def grafico()` [L26-L30]

### `graficos_matplotlib.py` (Python, 25 lines)
  - *(no top-level symbols extracted)*

### `pandas_dashboard.py` (Python, 85 lines)
  - `def carregar_dados()` [L7-L37]
  - `def calcular_rfm()` [L40-L54]
  - `def treinar_regressao_faturamento()` [L57-L68]

### `pandas_graficos.py` (Python, 51 lines)
  - *(no top-level symbols extracted)*

### `tests/test_dashboard_data.py` (Python, 26 lines)
  - `class DashboardDataTests(unittest.TestCase)` [L14-L26]
    - `def DashboardDataTests.test_carregar_csv_enviado_calcula_valor_liquido()` [L15-L18]
    - `def DashboardDataTests.test_carregar_csv_rejeita_colunas_ausentes()` [L20-L22]
    - `def DashboardDataTests.test_carregar_csv_rejeita_desconto_invalido()` [L24-L26]

### `tests/test_pipeline_demo.py` (Python, 5 lines)
  - `def calcular_total()` [L1-L2]
  - `def test_calcular_total()` [L4-L5]

### `tests/test_security_pipeline.py` (Python, 5 lines)
  - `def validar_desconto()` [L1-L2]
  - `def test_validar_desconto()` [L4-L5]
