from io import BytesIO
import unittest

from pandas_dashboard import carregar_dados


CABECALHO = (
    "id_venda,data,cliente,cidade,produto,categoria,quantidade,"
    "preco_unitario,desconto,metodo_pagamento,avaliacao\n"
)
LINHA = "1,2026-01-05,Ana,São Paulo,Notebook,Eletrônicos,2,100,0.1,PIX,5\n"


class DashboardDataTests(unittest.TestCase):
    def test_carregar_csv_enviado_calcula_valor_liquido(self) -> None:
        vendas = carregar_dados(BytesIO((CABECALHO + LINHA).encode()))
        self.assertAlmostEqual(vendas["valor_liquido"].iloc[0], 180)
        self.assertEqual(len(vendas), 1)

    def test_carregar_csv_rejeita_colunas_ausentes(self) -> None:
        with self.assertRaisesRegex(ValueError, "Colunas ausentes"):
            carregar_dados(BytesIO(b"id_venda,data\n1,2026-01-05\n"))

    def test_carregar_csv_rejeita_desconto_invalido(self) -> None:
        with self.assertRaisesRegex(ValueError, "fora do intervalo"):
            carregar_dados(BytesIO((CABECALHO + LINHA.replace(",0.1,", ",1.5,")).encode()))
