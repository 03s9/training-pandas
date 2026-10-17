import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def carregar_dados(caminho_csv: str = 'vendas_loja.csv') -> pd.DataFrame:
    df = pd.read_csv(caminho_csv, parse_dates=['data'])
    df = df.drop_duplicates(subset=['data', 'cliente', 'produto', 'quantidade'], keep='first').copy()
    df['avaliacao'] = df['avaliacao'].fillna(df['avaliacao'].median())

    df['valor_bruto'] = df['quantidade'] * df['preco_unitario']
    df['valor_liquido'] = df['valor_bruto'] * (1 - df['desconto'])
    df['porte'] = np.select(
        [df['valor_bruto'] < 1000, df['valor_bruto'] < 3000],
        ['baixa', 'media'],
        default='alta'
    )
    df['mes'] = df['data'].dt.month
    df['ano'] = df['data'].dt.year
    return df


def calcular_rfm(df: pd.DataFrame) -> pd.DataFrame:
    data_referencia = df['data'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('cliente').agg(
        recencia_dias=('data', lambda x: (data_referencia - x.max()).days),
        frequencia=('id_venda', 'count'),
        monetario=('valor_liquido', 'sum')
    ).reset_index()

    condicoes = [
        (rfm['monetario'] >= 4000) | (rfm['frequencia'] >= 2),
        (rfm['recencia_dias'] <= 20) & (rfm['monetario'] >= 1500)
    ]
    segmentos = ['Cliente VIP', 'Potencial Lealdade']
    rfm['segmento'] = np.select(condicoes, segmentos, default='Regular / Em Risco')
    return rfm.sort_values(by='monetario', ascending=False)


def treinar_regressao_faturamento(df: pd.DataFrame):
    vendas_diarias = df.groupby('data')['valor_liquido'].sum().reset_index()
    vendas_diarias['dias_corridos'] = (vendas_diarias['data'] - vendas_diarias['data'].min()).dt.days

    X = vendas_diarias[['dias_corridos']]
    y = vendas_diarias['valor_liquido']

    modelo = LinearRegression()
    modelo.fit(X, y)

    vendas_diarias['tendencia_prevista'] = modelo.predict(X)
    return vendas_diarias, modelo


VendasLoja = carregar_dados()
RFM_Clientes = calcular_rfm(VendasLoja)
TendenciaVendas, ModeloRegressao = treinar_regressao_faturamento(VendasLoja)

if __name__ == '__main__':
    print("--- RESUMO DO DATAFRAME TRATADO ---")
    print(VendasLoja.head(5))

    print("\n--- SEGMENTAÇÃO RFM DE CLIENTES (TOP 10) ---")
    print(RFM_Clientes.head(10).to_string(index=False))

    proximo_dia = pd.DataFrame({'dias_corridos': [TendenciaVendas['dias_corridos'].max() + 7]})
    previsao_7d = ModeloRegressao.predict(proximo_dia)[0]
    print("\n--- REGRESSÃO LINEAR ---")
    print(f"Previsão de tendência diária (+7 dias): R$ {previsao_7d:,.2f}")
