# REPO_MAP.md — Mapa Neural de Símbolos e Conexões

> Atualizado em: `2026-11-08 22:45:56`
> **Instrução para IAs (Antigravity, Cursor, Codex)**: Use os intervalos `[L<inicio>-L<fim>]` abaixo para ler apenas as linhas necessárias (`StartLine`/`EndLine`). Nunca leia arquivos inteiros grandes sem consultar este mapa.

**Resumo do Grafo**: `13` arquivos indexados | `45` símbolos mapeados.

### `api.py` (Python, 154 lines)
  - `def get_dataset()` [L28-L35]
  - `def filtered()` [L38-L53]
  - `def records()` [L56-L57]
  - @app.post('/api/datasets') -> `async def upload_dataset()` [L61-L75]
  - @app.get('/api/dashboard/{dataset_id}') -> `def dashboard()` [L79-L114]
  - @app.get('/api/advanced/{dataset_id}') -> `def advanced()` [L118-L154]

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

### `tests/test_api.py` (Python, 38 lines)
  - `def test_upload_filters_and_advanced()` [L16-L25]
  - `def test_invalid_upload_and_expired_session()` [L28-L31]
  - `def test_empty_and_insufficient_states()` [L34-L38]

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

### `web/vite.config.ts` (TypeScript, 7 lines)
  - *(no top-level symbols extracted)*

### `web/src/App.tsx` (React/TSX, 235 lines)
  - `fn/component money` [L9]
  - `fn/component number` [L12]
  - `type Row` [L14]
  - `type Dashboard` [L18]
  - `type Filters` [L27]
  - `type AppState` [L28]
  - `function useApp` [L36]
  - `function query` [L41]
  - `async function readError` [L49]
  - `function Provider` [L54]
  - `function Header` [L85]
  - `function Footer` [L97]
  - `function Landing` [L101]
  - `function Notice` [L135]
  - `function FiltersPanel` [L139]
  - `async function upload` [L143]
  - `function Shell` [L169]
  - `function DashboardPage` [L173]
  - `type Advanced` [L200]
  - `function AdvancedPage` [L201]
  - `function App` [L233]

### `web/src/Plot3D.tsx` (React/TSX, 35 lines)
  - `type Point` [L4]
  - `function Plot3D` [L5]

### `web/src/main.tsx` (React/TSX, 9 lines)
  - *(no top-level symbols extracted)*
