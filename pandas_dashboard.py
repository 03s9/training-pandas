import pandas as pd
import numpy as np

VendasLoja = pd.read_csv('vendas_loja.csv', parse_dates=['data'])

print("Aqui estão as 6 primeiras linhas do dataframe:")
print(VendasLoja.head(6))

print("\nAqui estão as 6 últimas linhas do dataframe:")
print(VendasLoja.tail(6))

# Definições gerais de estatistica descritiva
print("\nAqui estão as informações do dataframe:")
print(VendasLoja.info())

print("\nAqui estão as estatísticas descritivas do dataframe:")
print(VendasLoja.describe())

# Tratamento de dados - checando duplicatas
duplicados = VendasLoja[VendasLoja.duplicated(subset=['data', 'cliente', 'produto', 'quantidade'], keep=False)]
print("\nNecessário tratamento de duplicatas: ")
print(duplicados)
VendasLoja = VendasLoja.drop_duplicates(subset=['data', 'cliente', 'produto', 'quantidade'], keep='first').copy()

# Tratamento de dados - checando valores nulos
valores_nulos = VendasLoja[VendasLoja.isnull().any(axis=1)]
print("\nNecessário tratamento de valores nulos: ")
print(valores_nulos)
VendasLoja['avaliacao'] = VendasLoja['avaliacao'].fillna(VendasLoja['avaliacao'].median())

VendasLoja['valor_bruto'] = VendasLoja['quantidade'] * VendasLoja['preco_unitario']

VendasLoja['porte'] = np.select(
    [VendasLoja['valor_bruto'] < 5000, VendasLoja['valor_bruto'] < 10000],
    ['baixa', 'media'],
    default='alta'
)

print("\nAqui estão as categorias das vendas:")
print(VendasLoja['categoria'].value_counts())

VendasLoja['valor_liquido'] = VendasLoja['valor_bruto'] * (1 - VendasLoja['desconto'])

VendasLoja['mes'] = VendasLoja['data'].dt.month
VendasLoja['ano'] = VendasLoja['data'].dt.year

filtro_sp = VendasLoja[(VendasLoja['cidade'] == 'São Paulo') & (VendasLoja['valor_liquido'] > 1000)]
print("\nVendas em SP estão no valor de: ")
print(filtro_sp['valor_liquido'].sum())

print(filtro_sp[['id_venda', 'valor_liquido', 'produto', 'cliente']])

filtro_pix = VendasLoja[(VendasLoja['metodo_pagamento'] == 'PIX') & (VendasLoja['categoria'].isin(['Eletrônicos', 'Hardware']))]
print("\nVendas via PIX (Eletrônicos e Hardware):")
print(filtro_pix[['id_venda', 'cliente', 'categoria', 'valor_liquido']])
