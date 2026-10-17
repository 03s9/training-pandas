import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pandas_dashboard import VendasLoja, calcular_rfm, treinar_regressao_faturamento

st.set_page_config(page_title="Dashboard de Vendas & Data Science", page_icon="📊", layout="wide")

st.title("📊 Dashboard Interativo de Vendas, RFM & Regressão")

st.sidebar.header("🔍 Filtros")
cidades = st.sidebar.multiselect(
    "Cidade",
    options=VendasLoja['cidade'].unique(),
    default=VendasLoja['cidade'].unique()
)
categorias = st.sidebar.multiselect(
    "Categoria",
    options=VendasLoja['categoria'].unique(),
    default=VendasLoja['categoria'].unique()
)

df_filtrado = VendasLoja[
    (VendasLoja['cidade'].isin(cidades)) &
    (VendasLoja['categoria'].isin(categorias))
]

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Faturamento Líquido", f"R$ {df_filtrado['valor_liquido'].sum():,.2f}")
col2.metric("🛒 Total de Pedidos", f"{len(df_filtrado)}")
col3.metric("📦 Itens Vendidos", f"{df_filtrado['quantidade'].sum()}")
col4.metric("⭐ Avaliação Média", f"{df_filtrado['avaliacao'].mean():.2f} / 5.0")

st.divider()

aba1, aba2, aba3, aba4 = st.tabs([
    "📈 Visão Geral & 3D",
    "🔥 Correlação & Boxplot",
    "🏆 Clientes RFM",
    "🤖 Previsão (Regressão)"
])

with aba1:
    c1, c2 = st.columns(2)
    with c1:
        fat_cat = df_filtrado.groupby('categoria')['valor_liquido'].sum().reset_index()
        fig_bar = px.bar(fat_cat, x='categoria', y='valor_liquido', color='categoria', title="Faturamento por Categoria")
        st.plotly_chart(fig_bar, use_container_width=True)
    with c2:
        fig_3d = px.scatter_3d(
            df_filtrado,
            x='quantidade',
            y='preco_unitario',
            z='avaliacao',
            color='categoria',
            size='valor_liquido',
            hover_name='produto',
            hover_data=['cliente', 'cidade'],
            title="Visão 3D Interativa: Qtd vs Preço vs Avaliação"
        )
        st.plotly_chart(fig_3d, use_container_width=True)

with aba2:
    c1, c2 = st.columns(2)
    with c1:
        cols_corr = ['quantidade', 'preco_unitario', 'desconto', 'avaliacao', 'valor_liquido']
        corr = df_filtrado[cols_corr].corr()
        fig_heat = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", title="Mapa de Calor de Correlação (Heatmap)")
        st.plotly_chart(fig_heat, use_container_width=True)
    with c2:
        fig_box = px.box(df_filtrado, x='categoria', y='valor_liquido', color='categoria', points="all", title="Boxplot de Valores e Outliers")
        st.plotly_chart(fig_box, use_container_width=True)

with aba3:
    rfm_df = calcular_rfm(df_filtrado)
    c1, c2 = st.columns([1, 1])
    with c1:
        fig_rfm = px.bar(rfm_df, x='cliente', y='monetario', color='segmento', title="Ranking RFM de Clientes")
        st.plotly_chart(fig_rfm, use_container_width=True)
    with c2:
        st.subheader("Tabela de Segmentação RFM")
        st.dataframe(rfm_df, use_container_width=True, hide_index=True)

with aba4:
    if len(df_filtrado) >= 2:
        tendencia_df, modelo = treinar_regressao_faturamento(df_filtrado)
        fig_reg = go.Figure()
        fig_reg.add_trace(go.Scatter(x=tendencia_df['data'], y=tendencia_df['valor_liquido'], mode='markers+lines', name='Faturamento Real'))
        fig_reg.add_trace(go.Scatter(x=tendencia_df['data'], y=tendencia_df['tendencia_prevista'], mode='lines', name='Tendência (Regressão Linear)', line=dict(color='red', width=3)))
        fig_reg.update_layout(title="Regressão Linear do Faturamento Diário", xaxis_title="Data", yaxis_title="Valor Líquido (R$)")
        st.plotly_chart(fig_reg, use_container_width=True)

        dias_futuros = st.slider("Simular previsão para daqui a quantos dias?", 1, 60, 15)
        dia_alvo = pd.DataFrame({'dias_corridos': [tendencia_df['dias_corridos'].max() + dias_futuros]})
        valor_previsto = modelo.predict(dia_alvo)[0]
        st.info(f"🔮 Tendência estimada pelo modelo para **+{dias_futuros} dias**: **R$ {max(0, valor_previsto):,.2f}**")
    else:
        st.warning("Selecione mais dados nos filtros para calcular a regressão.")
