import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from pandas_dashboard import carregar_dados, calcular_rfm, treinar_regressao_faturamento

st.set_page_config(page_title="Visão de vendas | Training Pandas", layout="wide")
st.markdown("""
<style>
.stApp {background: #f8fafc; color: #1e293b;}
.block-container {max-width: 1440px; padding-top: 2rem;}
h1, h2, h3 {color: #1e3a8a; letter-spacing: -.025em;}
[data-testid="stMetric"] {background: #fff; border: 1px solid #dbeafe; border-radius: 12px; padding: 18px; min-height: 130px;}
[data-testid="stMetricValue"] {font-variant-numeric: tabular-nums; color: #1e40af;}
:focus-visible {outline: 3px solid #d97706 !important; outline-offset: 2px;}
@media (max-width: 640px) {.block-container {padding: 1rem;}}
</style>
""", unsafe_allow_html=True)


def moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def grafico(fig: go.Figure) -> None:
    fig.update_layout(template="plotly_white", font=dict(color="#1e293b"),
                      paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                      margin=dict(l=16, r=16, t=56, b=16), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)


st.sidebar.title("Fonte e filtros")
arquivo = st.sidebar.file_uploader(
    "Carregar vendas em CSV", type="csv",
    help="Use as colunas do arquivo de exemplo vendas_loja.csv. O arquivo é usado nesta sessão.",
)
try:
    vendas = carregar_dados(arquivo) if arquivo is not None else carregar_dados()
except (ValueError, UnicodeError, pd.errors.ParserError) as erro:
    st.error(f"Não foi possível carregar o CSV: {erro}")
    st.stop()
st.sidebar.caption("Base real carregada" if arquivo else f"Base de demonstração · {len(vendas)} vendas")

inicio, fim = vendas["data"].min().date(), vendas["data"].max().date()
periodo = st.sidebar.date_input("Período", value=(inicio, fim),
                                min_value=inicio, max_value=fim)
cidades = st.sidebar.multiselect("Cidades", sorted(vendas["cidade"].dropna().unique()),
                                 default=sorted(vendas["cidade"].dropna().unique()))
categorias = st.sidebar.multiselect("Categorias", sorted(vendas["categoria"].dropna().unique()),
                                    default=sorted(vendas["categoria"].dropna().unique()))
if len(periodo) != 2:
    st.info("Selecione as duas datas do período para ver o painel.")
    st.stop()

filtrado = vendas.loc[
    vendas["data"].dt.date.between(*periodo)
    & vendas["cidade"].isin(cidades)
    & vendas["categoria"].isin(categorias)
].copy()

st.caption("TRAINING PANDAS  /  INTELIGÊNCIA DE VENDAS")
st.title("Visão de vendas")
st.caption(f"{periodo[0]:%d/%m/%Y} – {periodo[1]:%d/%m/%Y} · "
           f"{len(filtrado):,} vendas · "
           f"{'Base real' if arquivo else 'Dados de demonstração'}")
pagina = st.radio("Seção", ["Visão geral", "Análises avançadas"], horizontal=True)
if filtrado.empty:
    st.info("Nenhuma venda corresponde aos filtros. Ajuste o período, as cidades ou as categorias.")
    st.stop()

if pagina == "Visão geral":
    kpis = st.columns(4)
    kpis[0].metric("Faturamento líquido", moeda(filtrado["valor_liquido"].sum()))
    kpis[1].metric("Pedidos", f"{len(filtrado):,}")
    kpis[2].metric("Ticket médio", moeda(filtrado["valor_liquido"].mean()))
    kpis[3].metric("Itens vendidos", f"{filtrado['quantidade'].sum():,.0f}")

    diario = filtrado.groupby("data", as_index=False)["valor_liquido"].sum().sort_values("data")
    fig = px.line(diario, x="data", y="valor_liquido", markers=True,
                  title="Faturamento ao longo do tempo",
                  labels={"data": "Data", "valor_liquido": "Faturamento líquido (R$)"})
    fig.update_traces(line_color="#1e40af", marker_color="#d97706")
    with st.container(border=True):
        grafico(fig)
        with st.expander("Ver valores por dia"):
            st.dataframe(diario, width="stretch", hide_index=True)

    esquerda, direita = st.columns(2)
    for coluna, nome, cor, alvo in (
        ("categoria", "Faturamento por categoria", "#1e40af", esquerda),
        ("cidade", "Faturamento por cidade", "#3b82f6", direita),
    ):
        with alvo, st.container(border=True):
            resumo = (filtrado.groupby(coluna, as_index=False)["valor_liquido"]
                      .sum().sort_values("valor_liquido"))
            fig = px.bar(resumo, x="valor_liquido", y=coluna, orientation="h",
                         text="valor_liquido", title=nome,
                         labels={coluna: coluna.title(),
                                 "valor_liquido": "Faturamento líquido (R$)"})
            fig.update_traces(marker_color=cor, texttemplate="R$ %{x:,.0f}")
            grafico(fig)

    st.subheader("Vendas do período")
    st.dataframe(
        filtrado[["data", "id_venda", "cidade", "categoria", "produto",
                  "quantidade", "valor_liquido"]].sort_values("data", ascending=False),
        width="stretch", hide_index=True,
    )
else:
    analise = st.selectbox(
        "Análise", ["Clientes RFM", "Tendência e previsão",
                    "Distribuição e correlação", "Exploração 3D"],
    )
    if analise == "Clientes RFM":
        rfm = calcular_rfm(filtrado)
        grafico(px.bar(rfm, x="cliente", y="monetario", color="segmento",
                       title="Valor por cliente e segmento RFM",
                       labels={"cliente": "Cliente", "monetario": "Valor líquido (R$)"}))
        st.dataframe(rfm, width="stretch", hide_index=True)
    elif analise == "Tendência e previsão":
        if filtrado["data"].nunique() < 2:
            st.info("Selecione vendas de pelo menos dois dias para calcular a tendência.")
        else:
            tendencia, modelo = treinar_regressao_faturamento(filtrado)
            fig = go.Figure()
            fig.add_scatter(x=tendencia["data"], y=tendencia["valor_liquido"],
                            mode="lines+markers", name="Faturamento real")
            fig.add_scatter(x=tendencia["data"], y=tendencia["tendencia_prevista"],
                            mode="lines", name="Tendência linear",
                            line=dict(color="#d97706", dash="dash"))
            fig.update_layout(title="Faturamento diário e tendência linear",
                              xaxis_title="Data", yaxis_title="Valor líquido (R$)")
            grafico(fig)
            dias = st.slider("Dias à frente", 1, 60, 15)
            alvo = pd.DataFrame({"dias_corridos": [tendencia["dias_corridos"].max() + dias]})
            st.metric(f"Estimativa para +{dias} dias", moeda(max(0, modelo.predict(alvo)[0])))
            st.caption("Estimativa exploratória por regressão linear. Não é uma meta nem uma previsão garantida.")
    elif analise == "Distribuição e correlação":
        colunas = ["quantidade", "preco_unitario", "desconto", "avaliacao", "valor_liquido"]
        esquerda, direita = st.columns(2)
        with esquerda:
            grafico(px.imshow(filtrado[colunas].corr(), text_auto=".2f",
                              color_continuous_scale="RdBu_r",
                              title="Correlação entre indicadores"))
        with direita:
            grafico(px.box(filtrado, x="categoria", y="valor_liquido", points="all",
                           title="Distribuição do valor por categoria"))
    else:
        st.caption("Arraste para girar; use o zoom para inspecionar os pontos.")
        grafico(px.scatter_3d(
            filtrado, x="quantidade", y="preco_unitario", z="avaliacao",
            color="categoria", size="valor_liquido", hover_name="produto",
            hover_data=["cidade"], title="Quantidade × preço × avaliação",
        ))
        st.dataframe(filtrado[["produto", "categoria", "quantidade",
                               "preco_unitario", "avaliacao", "valor_liquido"]],
                     width="stretch", hide_index=True)
