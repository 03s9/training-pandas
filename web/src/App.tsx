import { createContext, lazy, Suspense, useContext, useEffect, useState } from 'react'
import { Link, NavLink, Route, Routes } from 'react-router-dom'
import {
  Area, AreaChart, Bar, BarChart, CartesianGrid, Legend, Line, LineChart,
  ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts'

const Plot3D = lazy(() => import('./Plot3D'))
const money = (value: number) => new Intl.NumberFormat('pt-BR', {
  style: 'currency', currency: 'BRL', maximumFractionDigits: 0,
}).format(value)
const number = (value: number) => new Intl.NumberFormat('pt-BR').format(value)

type Row = {
  data: string; id_venda: number; cidade: string; categoria: string;
  produto: string; quantidade: number; valor_liquido: number
}
type Dashboard = {
  source: 'demo' | 'upload'
  options: { cities: string[]; categories: string[]; min_date: string; max_date: string }
  kpis: { revenue: number; orders: number; ticket: number; items: number }
  daily: { date: string; value: number }[]
  categories: { name: string; value: number }[]
  cities: { name: string; value: number }[]
  rows: Row[]; total_rows: number
}
type Filters = { start: string; end: string; city: string; category: string }
type AppState = {
  dataset: string; setDataset: (value: string) => void
  filters: Filters; setFilters: (value: Filters) => void
  data: Dashboard | null; loading: boolean; error: string
  page: number; setPage: (value: number) => void
  reload: () => void
}
const Context = createContext<AppState | null>(null)
function useApp() {
  const state = useContext(Context)
  if (!state) throw new Error('Contexto ausente')
  return state
}
function query(filters: Filters) {
  const params = new URLSearchParams()
  if (filters.start) params.set('start', filters.start)
  if (filters.end) params.set('end', filters.end)
  if (filters.city) params.append('cities', filters.city)
  if (filters.category) params.append('categories', filters.category)
  return params
}
async function readError(response: Response) {
  const body = await response.json().catch(() => null) as { detail?: string } | null
  return body?.detail || `Erro HTTP ${response.status}`
}

function Provider({ children }: { children: React.ReactNode }) {
  const [dataset, setDataset] = useState('demo')
  const [filters, setFilters] = useState<Filters>({ start: '', end: '', city: '', category: '' })
  const [data, setData] = useState<Dashboard | null>(null)
  const [page, setPage] = useState(1)
  const [reloadKey, reload] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    setError('')
    const params = query(filters)
    params.set('page', String(page))
    fetch(`/api/dashboard/${dataset}?${params}`, { signal: controller.signal })
      .then(async response => {
        if (!response.ok) throw new Error(await readError(response))
        return response.json() as Promise<Dashboard>
      })
      .then(setData)
      .catch(err => { if (!controller.signal.aborted) setError(String(err.message)) })
      .finally(() => { if (!controller.signal.aborted) setLoading(false) })
    return () => controller.abort()
  }, [dataset, filters, page, reloadKey])
  return <Context.Provider value={{
    dataset, setDataset: value => { setDataset(value); setPage(1); setFilters({ start: '', end: '', city: '', category: '' }) },
    filters, setFilters: value => { setFilters(value); setPage(1) },
    data, loading, error, page, setPage, reload: () => reload(n => n + 1),
  }}>{children}</Context.Provider>
}

function Header() {
  return <header className="site-header">
    <Link className="brand" to="/"><span className="brand-mark">TP</span><span>training<span className="brand-accent">pandas</span></span></Link>
    <nav aria-label="Navegação principal">
      <NavLink to="/" end>Projeto</NavLink>
      <NavLink to="/dashboard">Dashboard</NavLink>
      <NavLink to="/analises">Análises</NavLink>
    </nav>
    <Link className="header-cta" to="/dashboard">Abrir painel <span aria-hidden="true">↗</span></Link>
  </header>
}

function Footer() {
  return <footer className="footer"><span>Training Pandas · Análise de vendas com Python</span><span>Projeto de Vitor Góngora · 2026</span></footer>
}

function Landing() {
  return <>
    <section className="hero">
      <div className="hero-copy">
        <div className="eyebrow"><span className="status-dot" /> PROJETO DE DATA SCIENCE</div>
        <h1>Dados de vendas.<br /><em>Decisões mais claras.</em></h1>
        <p>Do CSV à visão gerencial: um projeto que transforma transações em indicadores, tendências e análises de clientes.</p>
        <div className="hero-actions">
          <Link className="button primary" to="/dashboard">Explorar dashboard <span aria-hidden="true">↗</span></Link>
          <a className="button secondary" href="https://github.com/03s9/training-pandas" target="_blank" rel="noreferrer">Ver código no GitHub</a>
        </div>
        <div className="hero-meta"><span>01 / Pipeline em Python</span><span>02 / Visualização interativa</span><span>03 / RFM + regressão</span></div>
      </div>
      <div className="preview" aria-label="Prévia ilustrativa do painel">
        <div className="preview-top"><span className="preview-label">VISÃO GERAL</span><span className="live"><span className="status-dot" /> Demonstração</span></div>
        <div className="preview-number">R$ 36.995<span>,93</span></div>
        <div className="preview-sub">Faturamento líquido · base de demonstração</div>
        <div className="preview-bars" aria-hidden="true">{[36,54,42,76,58,88,66,100,73,90,65,84].map((height, index) => <i key={index} style={{ height: `${height}%` }} />)}</div>
        <div className="preview-bottom"><span>JAN</span><span>FEV 2026</span></div>
        <div className="preview-chip">+ Insights por cidade e categoria</div>
      </div>
    </section>
    <section className="section landing-section">
      <div className="section-heading"><span className="eyebrow">O PROJETO</span><h2>Uma análise completa, do dado à ação.</h2><p>Uma experiência pensada para quem precisa entender o negócio sem perder acesso à profundidade técnica.</p></div>
      <div className="feature-grid">
        <article className="feature-card feature-large"><span className="feature-index">01 / GESTÃO</span><h3>O essencial primeiro.</h3><p>Faturamento, pedidos, ticket médio e evolução temporal em uma visão feita para leitura rápida.</p><div className="feature-line" /></article>
        <article className="feature-card"><span className="feature-index">02 / CLIENTES</span><h3>Segmentação RFM.</h3><p>Recência, frequência e valor para identificar grupos de clientes.</p></article>
        <article className="feature-card"><span className="feature-index">03 / TENDÊNCIA</span><h3>Regressão exploratória.</h3><p>Uma leitura do histórico com estimativas apresentadas com contexto.</p></article>
      </div>
    </section>
    <section className="stack-band"><div><span className="eyebrow">CONSTRUÍDO COM</span><h2>Python na análise.<br />Clareza na interface.</h2></div><p>Pandas · scikit-learn · FastAPI · React · Recharts · Plotly</p><Link className="button primary" to="/dashboard">Entrar no painel <span aria-hidden="true">↗</span></Link></section>
  </>
}

function Notice({ kind, children, retry }: { kind: 'error' | 'empty' | 'loading'; children: React.ReactNode; retry?: () => void }) {
  return <div className={`notice ${kind}`} role={kind === 'error' ? 'alert' : 'status'}><p>{children}</p>{retry && <button className="button secondary" onClick={retry}>Tentar novamente</button>}</div>
}

function FiltersPanel() {
  const { data, filters, setFilters, setDataset, reload } = useApp()
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')
  async function upload(file?: File) {
    if (!file) return
    setUploading(true); setUploadError('')
    const form = new FormData()
    form.append('file', file)
    try {
      const response = await fetch('/api/datasets', { method: 'POST', body: form })
      if (!response.ok) throw new Error(await readError(response))
      const body = await response.json() as { dataset_id: string }
      setDataset(body.dataset_id)
    } catch (err) { setUploadError(err instanceof Error ? err.message : 'Falha no upload') }
    finally { setUploading(false) }
  }
  return <aside className="filters">
    <div className="filter-heading"><span className="eyebrow">CONTROLES</span><h2>Refine os dados</h2><p>Os filtros atualizam todas as análises.</p></div>
    <label className="upload-box"><span className="upload-icon">↑</span><strong>{uploading ? 'Enviando…' : 'Carregar CSV real'}</strong><small>Até 10 MB e 10 mil vendas</small><input type="file" accept=".csv,text/csv" disabled={uploading} onChange={event => upload(event.target.files?.[0])} /></label>
    {uploadError && <p className="field-error" role="alert">{uploadError}</p>}
    <div className="source-pill"><span className="status-dot" /> {data?.source === 'upload' ? 'Base enviada nesta sessão' : 'Base de demonstração'}</div>
    <div className="filter-group"><label htmlFor="start">Data inicial</label><input id="start" type="date" min={data?.options.min_date} max={data?.options.max_date} value={filters.start} onChange={e => setFilters({ ...filters, start: e.target.value })} /></div>
    <div className="filter-group"><label htmlFor="end">Data final</label><input id="end" type="date" min={data?.options.min_date} max={data?.options.max_date} value={filters.end} onChange={e => setFilters({ ...filters, end: e.target.value })} /></div>
    <div className="filter-group"><label htmlFor="city">Cidade</label><select id="city" value={filters.city} onChange={e => setFilters({ ...filters, city: e.target.value })}><option value="">Todas as cidades</option>{data?.options.cities.map(city => <option key={city}>{city}</option>)}</select></div>
    <div className="filter-group"><label htmlFor="category">Categoria</label><select id="category" value={filters.category} onChange={e => setFilters({ ...filters, category: e.target.value })}><option value="">Todas as categorias</option>{data?.options.categories.map(category => <option key={category}>{category}</option>)}</select></div>
    <button className="reset-button" onClick={() => { setFilters({ start: '', end: '', city: '', category: '' }); reload() }}>Limpar filtros <span aria-hidden="true">↺</span></button>
  </aside>
}

function Shell({ title, description, children }: { title: string; description: string; children: React.ReactNode }) {
  return <div className="app-shell"><FiltersPanel /><main className="workspace"><div className="workspace-heading"><div><span className="eyebrow">INTELIGÊNCIA DE VENDAS / 2026</span><h1>{title}</h1><p>{description}</p></div><div className="workspace-nav"><NavLink to="/dashboard">Visão geral</NavLink><NavLink to="/analises">Análises avançadas</NavLink></div></div>{children}</main></div>
}

function DashboardPage() {
  const { data, loading, error, reload, page, setPage } = useApp()
  return <Shell title="Visão geral" description="Uma leitura clara do desempenho comercial.">
    {loading ? <Notice kind="loading">Carregando indicadores…</Notice> :
      error ? <Notice kind="error" retry={reload}>{error}</Notice> :
      data && <>
        <div className="data-caption"><span className="status-dot" /> {data.source === 'demo' ? 'Dados de demonstração' : 'CSV enviado'} <span>· {number(data.total_rows)} vendas no recorte</span></div>
        {data.total_rows === 0 ? <Notice kind="empty">Nenhuma venda corresponde aos filtros. Ajuste o período, a cidade ou a categoria.</Notice> : <>
          <div className="kpi-grid">
            {[
              ['Faturamento líquido', money(data.kpis.revenue), 'Receita após descontos'],
              ['Pedidos', number(data.kpis.orders), 'Transações no período'],
              ['Ticket médio', money(data.kpis.ticket), 'Por pedido'],
              ['Itens vendidos', number(data.kpis.items), 'Volume total'],
            ].map(([label, value, hint], index) => <article className={`kpi-card kpi-${index}`} key={label}><span>{label}</span><strong>{value}</strong><small>{hint}</small></article>)}
          </div>
          <div className="chart-grid">
            <section className="panel panel-wide"><div className="panel-heading"><div><span className="eyebrow">EVOLUÇÃO</span><h2>Faturamento ao longo do tempo</h2></div><span className="panel-tag">R$ · por dia</span></div><div className="chart"><ResponsiveContainer width="100%" height="100%"><AreaChart data={data.daily}><defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#3b82f6" stopOpacity={0.32} /><stop offset="100%" stopColor="#3b82f6" stopOpacity={0} /></linearGradient></defs><CartesianGrid stroke="#e8edf5" vertical={false} /><XAxis dataKey="date" tickFormatter={v => String(v).slice(5)} /><YAxis tickFormatter={v => number(Number(v) / 1000) + 'k'} /><Tooltip formatter={value => money(Number(value))} /><Area type="monotone" dataKey="value" name="Faturamento" stroke="#2563eb" fill="url(#area)" strokeWidth={3} /></AreaChart></ResponsiveContainer></div></section>
            <section className="panel"><div className="panel-heading"><div><span className="eyebrow">MIX DE VENDAS</span><h2>Por categoria</h2></div></div><div className="chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={data.categories} layout="vertical" margin={{ left: 8, right: 12 }}><CartesianGrid stroke="#e8edf5" horizontal={false} /><XAxis type="number" tickFormatter={v => number(Number(v) / 1000) + 'k'} /><YAxis dataKey="name" type="category" width={90} /><Tooltip formatter={value => money(Number(value))} /><Bar dataKey="value" name="Faturamento" fill="#2563eb" radius={[0, 5, 5, 0]} /></BarChart></ResponsiveContainer></div></section>
            <section className="panel"><div className="panel-heading"><div><span className="eyebrow">REGIÕES</span><h2>Por cidade</h2></div></div><div className="chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={data.cities} layout="vertical" margin={{ left: 8, right: 12 }}><CartesianGrid stroke="#e8edf5" horizontal={false} /><XAxis type="number" tickFormatter={v => number(Number(v) / 1000) + 'k'} /><YAxis dataKey="name" type="category" width={108} tick={{ fontSize: 11 }} /><Tooltip formatter={value => money(Number(value))} /><Bar dataKey="value" name="Faturamento" fill="#0f172a" radius={[0, 5, 5, 0]} /></BarChart></ResponsiveContainer></div></section>
          </div>
          <section className="panel table-panel"><div className="panel-heading"><div><span className="eyebrow">DETALHE</span><h2>Vendas do período</h2></div><span className="panel-tag">{number(data.total_rows)} registros</span></div><div className="table-wrap"><table><thead><tr><th>Data</th><th>Pedido</th><th>Cidade</th><th>Categoria</th><th>Produto</th><th>Itens</th><th>Valor líquido</th></tr></thead><tbody>{data.rows.map(row => <tr key={row.id_venda}><td>{new Date(row.data + 'T12:00:00').toLocaleDateString('pt-BR')}</td><td>#{row.id_venda}</td><td>{row.cidade}</td><td>{row.categoria}</td><td>{row.produto}</td><td>{row.quantidade}</td><td>{money(row.valor_liquido)}</td></tr>)}</tbody></table></div><div className="pagination"><button disabled={page === 1} onClick={() => setPage(page - 1)}>Anterior</button><span>Página {page} de {Math.ceil(data.total_rows / 20)}</span><button disabled={page * 20 >= data.total_rows} onClick={() => setPage(page + 1)}>Próxima</button></div></section>
        </>}
      </>}
  </Shell>
}

type Advanced = { status: string; rows?: Record<string, string | number>[]; estimate?: number; columns?: string[]; matrix?: (number | null)[][]; points?: Record<string, string | number>[]; total?: number }
function AdvancedPage() {
  const { dataset, filters, data } = useApp()
  const [analysis, setAnalysis] = useState('rfm')
  const [days, setDays] = useState(15)
  const [result, setResult] = useState<Advanced | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [reloadKey, reload] = useState(0)
  useEffect(() => {
    const controller = new AbortController()
    setLoading(true); setError('')
    const params = query(filters); params.set('analysis', analysis); params.set('days', String(days))
    fetch(`/api/advanced/${dataset}?${params}`, { signal: controller.signal })
      .then(async response => { if (!response.ok) throw new Error(await readError(response)); return response.json() as Promise<Advanced> })
      .then(setResult)
      .catch(err => { if (!controller.signal.aborted) setError(String(err.message)) })
      .finally(() => { if (!controller.signal.aborted) setLoading(false) })
    return () => controller.abort()
  }, [dataset, filters, analysis, days, reloadKey])
  return <Shell title="Análises avançadas" description="Explore clientes, tendências e relações entre variáveis.">
    <div className="analysis-tabs" role="group" aria-label="Tipo de análise">{[['rfm', 'Clientes RFM'], ['forecast', 'Tendência'], ['correlation', 'Correlação'], ['3d', 'Exploração 3D']].map(([key, label]) => <button key={key} className={analysis === key ? 'active' : ''} onClick={() => setAnalysis(key)} aria-pressed={analysis === key}>{label}</button>)}</div>
    {analysis === 'forecast' && <div className="days-control"><label htmlFor="days">Projetar quantos dias?</label><input id="days" type="range" min="1" max="60" value={days} onChange={e => setDays(Number(e.target.value))} /><strong>{days} dias</strong></div>}
    {error ? <Notice kind="error" retry={() => reload(n => n + 1)}>{error}</Notice> : loading ? <Notice kind="loading">Calculando análise…</Notice> : result?.status !== 'ok' ? <Notice kind="empty">{result?.status === 'insufficient' ? 'Selecione vendas em pelo menos dois dias para calcular a tendência.' : 'Nenhum dado corresponde aos filtros.'}</Notice> : <>
      {analysis === 'rfm' && <section className="panel"><div className="panel-heading"><div><span className="eyebrow">CLIENTES</span><h2>Segmentação RFM</h2></div></div><div className="table-wrap"><table><thead><tr><th>Cliente</th><th>Recência</th><th>Frequência</th><th>Valor</th><th>Segmento</th></tr></thead><tbody>{result.rows?.map(row => <tr key={String(row.cliente)}><td>{row.cliente}</td><td>{row.recencia_dias} dias</td><td>{row.frequencia}</td><td>{money(Number(row.monetario))}</td><td><span className="segment">{row.segmento}</span></td></tr>)}</tbody></table></div></section>}
      {analysis === 'forecast' && <><div className="estimate"><span>ESTIMATIVA EXPLORATÓRIA</span><strong>{money(result.estimate || 0)}</strong><p>Tendência linear para +{days} dias. Não é uma meta ou previsão garantida.</p></div><section className="panel"><div className="panel-heading"><h2>Faturamento diário e tendência</h2></div><div className="chart"><ResponsiveContainer width="100%" height="100%"><LineChart data={result.rows}><CartesianGrid stroke="#e8edf5" vertical={false} /><XAxis dataKey="date" /><YAxis /><Tooltip formatter={value => money(Number(value))} /><Legend /><Line dataKey="actual" name="Real" stroke="#2563eb" strokeWidth={2} /><Line dataKey="trend" name="Tendência" stroke="#f59e0b" strokeDasharray="5 4" strokeWidth={2} /></LineChart></ResponsiveContainer></div></section></>}
      {analysis === 'correlation' && <div className="chart-grid"><section className="panel"><div className="panel-heading"><h2>Matriz de correlação</h2></div><div className="table-wrap"><table className="matrix"><thead><tr><th>Variável</th>{result.columns?.map(name => <th key={name}>{name.replace('_', ' ')}</th>)}</tr></thead><tbody>{result.matrix?.map((row, index) => <tr key={index}><th>{result.columns?.[index].replace('_', ' ')}</th>{row.map((value, column) => <td key={column}>{value === null ? '—' : value.toFixed(2)}</td>)}</tr>)}</tbody></table></div></section><section className="panel"><div className="panel-heading"><h2>Ticket médio por categoria</h2></div><div className="chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={result.points}><CartesianGrid stroke="#e8edf5" vertical={false} /><XAxis dataKey="category" /><YAxis /><Tooltip formatter={value => money(Number(value))} /><Bar dataKey="value" fill="#2563eb" /></BarChart></ResponsiveContainer></div></section></div>}
      {analysis === '3d' && <section className="panel"><div className="panel-heading"><div><span className="eyebrow">EXPLORAÇÃO</span><h2>Quantidade × preço × avaliação</h2></div></div><p className="panel-note">Até 1.000 pontos no gráfico, de {number(result.total || 0)} vendas filtradas. Passe o cursor para ver os detalhes.</p><Suspense fallback={<Notice kind="loading">Carregando visualização 3D…</Notice>}><Plot3D points={result.points || []} /></Suspense><div className="table-wrap"><table><thead><tr><th>Produto</th><th>Categoria</th><th>Quantidade</th><th>Preço</th><th>Avaliação</th></tr></thead><tbody>{result.points?.slice(0, 20).map((row, index) => <tr key={index}><td>{row.produto}</td><td>{row.categoria}</td><td>{row.quantidade}</td><td>{money(Number(row.preco_unitario))}</td><td>{row.avaliacao}</td></tr>)}</tbody></table></div></section>}
      {data?.source === 'demo' && <p className="demo-note">Análises calculadas sobre a base de demonstração. Carregue um CSV real para trabalhar com seus dados.</p>}
    </>}
  </Shell>
}

export default function App() {
  return <Provider><Header /><Routes><Route path="/" element={<Landing />} /><Route path="/dashboard" element={<DashboardPage />} /><Route path="/analises" element={<AdvancedPage />} /></Routes><Footer /></Provider>
}
