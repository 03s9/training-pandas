<h1 align="center">📊 Pandas Dash + Graphics</h1>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="Pandas" src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img alt="NumPy" src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img alt="Seaborn" src="https://img.shields.io/badge/Seaborn-3776AB?style=for-the-badge" />
  <img alt="Matplotlib" src="https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge" />
</p>

> Projeto prático em Python utilizando **Pandas**, **NumPy**, **Matplotlib** e **Seaborn** para limpeza de dados, análise exploratória e geração de um dashboard visual de vendas.

---

## 🖼️ Preview do Dashboard

<p align="center">
  <img src="dashboard_vendas.png" alt="Dashboard de Vendas" width="800" />
</p>

---

## 🚀 O que o projeto faz

- **Limpeza e Tratamento (`pandas_dashboard.py`)**:
  - Leitura de dados em CSV (`vendas_loja.csv`) com conversão de datas (`datetime`).
  - Identificação e remoção de registros duplicados.
  - Tratamento de valores nulos (`NaN`) utilizando a mediana das avaliações.
  - Engenharia de atributos (*Feature Engineering*): cálculo de `valor_bruto`, `valor_liquido` (com descontos), classificação de porte da venda (`baixa`, `media`, `alta`), mês e ano.
  - Filtros avançados por cidade, método de pagamento (PIX) e categorias.
- **Visualização de Dados (`pandas_graficos.py`)**:
  - Gráfico de barras do faturamento líquido por categoria.
  - Gráfico de pizza da distribuição por método de pagamento.
  - Ranking de faturamento por cidade.
  - Série temporal com a evolução diária do faturamento.

---

## 📦 Instalação

Clone o repositório e instale as dependências:

```sh
git clone git@github.com:03s9/training-pandas.git
cd training-pandas
pip install -r requirements.txt
