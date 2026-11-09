from fastapi.testclient import TestClient

from api import app

client = TestClient(app)
HEADER = (
    "id_venda,data,cliente,cidade,produto,categoria,quantidade,"
    "preco_unitario,desconto,metodo_pagamento,avaliacao\n"
)
ROWS = (
    "1,2026-01-05,Ana,São Paulo,Notebook,Eletrônicos,2,100,0.1,PIX,5\n"
    "2,2026-01-06,Bia,Curitiba,Mouse,Acessórios,1,50,0,PIX,4\n"
)


def test_upload_filters_and_advanced() -> None:
    response = client.post("/api/datasets", files={"file": ("vendas.csv", HEADER + ROWS)})
    assert response.status_code == 200
    dataset = response.json()["dataset_id"]
    all_sales = client.get(f"/api/dashboard/{dataset}").json()
    assert all_sales["kpis"]["revenue"] == 230
    assert all_sales["kpis"]["orders"] == 2
    selected = client.get(f"/api/dashboard/{dataset}", params={"cities": "Curitiba"}).json()
    assert selected["kpis"]["revenue"] == 50
    assert client.get(f"/api/advanced/{dataset}", params={"analysis": "rfm"}).json()["status"] == "ok"


def test_invalid_upload_and_expired_session() -> None:
    response = client.post("/api/datasets", files={"file": ("vendas.csv", HEADER + ROWS.replace(",0.1,", ",1.5,"))})
    assert response.status_code == 422
    assert client.get("/api/dashboard/does-not-exist").status_code == 404


def test_empty_and_insufficient_states() -> None:
    empty = client.get("/api/advanced/demo", params={"analysis": "rfm", "cities": "Cidade inexistente"})
    assert empty.json()["status"] == "empty"
    one_day = client.get("/api/advanced/demo", params={"analysis": "forecast", "start": "2026-01-05", "end": "2026-01-05"})
    assert one_day.json()["status"] == "insufficient"
