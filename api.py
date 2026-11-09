"""API local do painel. Uploads vivem apenas na memória do processo."""
from datetime import date, datetime, timedelta, timezone
from io import BytesIO
import json
from pathlib import Path
from uuid import uuid4

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from pandas_dashboard import carregar_dados, calcular_rfm, treinar_regressao_faturamento

app = FastAPI(title="Training Pandas API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
BASE = Path(__file__).with_name("vendas_loja.csv")
# shortcut: armazenamento por processo; migrar para banco apenas se houver deploy multiusuário.
datasets: dict[str, tuple[pd.DataFrame, datetime]] = {
    "demo": (carregar_dados(str(BASE)), datetime.max.replace(tzinfo=timezone.utc))
}


def get_dataset(dataset_id: str) -> pd.DataFrame:
    now = datetime.now(timezone.utc)
    for key, (_, expiry) in list(datasets.items()):
        if expiry < now:
            del datasets[key]
    if dataset_id not in datasets:
        raise HTTPException(404, "Sessão expirada. Envie o CSV novamente.")
    return datasets[dataset_id][0]


def filtered(
    dataset_id: str, start: date | None, end: date | None,
    cities: list[str], categories: list[str],
) -> pd.DataFrame:
    df = get_dataset(dataset_id)
    if start and end and start > end:
        raise HTTPException(422, "Período inválido.")
    if start:
        df = df[df["data"].dt.date >= start]
    if end:
        df = df[df["data"].dt.date <= end]
    if cities:
        df = df[df["cidade"].isin(cities)]
    if categories:
        df = df[df["categoria"].isin(categories)]
    return df


def records(df: pd.DataFrame) -> list[dict]:
    return json.loads(df.to_json(orient="records", date_format="iso"))


@app.post("/api/datasets")
async def upload_dataset(file: UploadFile = File(...)) -> dict:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(422, "Envie um arquivo CSV.")
    data = await file.read(10_000_001)
    if len(data) > 10_000_000:
        raise HTTPException(413, "CSV excede 10 MB.")
    try:
        df = carregar_dados(BytesIO(data))
    except (ValueError, UnicodeError, pd.errors.ParserError) as error:
        raise HTTPException(422, str(error)) from error
    if len(df) > 10_000:
        raise HTTPException(413, "CSV excede 10 mil vendas.")
    key = uuid4().hex
    datasets[key] = (df, datetime.now(timezone.utc) + timedelta(hours=1))
    return {"dataset_id": key, "rows": len(df)}


@app.get("/api/dashboard/{dataset_id}")
def dashboard(
    dataset_id: str, start: date | None = None, end: date | None = None,
    cities: list[str] = Query(default=[]), categories: list[str] = Query(default=[]),
    page: int = Query(default=1, ge=1),
) -> dict:
    full = get_dataset(dataset_id)
    df = filtered(dataset_id, start, end, cities, categories)
    daily = df.groupby("data", as_index=False)["valor_liquido"].sum()
    by_category = df.groupby("categoria", as_index=False)["valor_liquido"].sum()
    by_city = df.groupby("cidade", as_index=False)["valor_liquido"].sum()
    table = df.sort_values("data", ascending=False).iloc[(page - 1) * 20:page * 20]
    columns = ["data", "id_venda", "cidade", "categoria", "produto", "quantidade", "valor_liquido"]
    return {
        "source": "demo" if dataset_id == "demo" else "upload",
        "options": {
            "cities": sorted(full["cidade"].dropna().unique().tolist()),
            "categories": sorted(full["categoria"].dropna().unique().tolist()),
            "min_date": full["data"].min().date().isoformat(),
            "max_date": full["data"].max().date().isoformat(),
        },
        "kpis": {
            "revenue": float(df["valor_liquido"].sum()),
            "orders": len(df),
            "ticket": float(df["valor_liquido"].mean()) if len(df) else 0,
            "items": int(df["quantidade"].sum()),
        },
        "daily": [{"date": row.data.date().isoformat(), "value": float(row.valor_liquido)}
                  for row in daily.itertuples()],
        "categories": [{"name": row.categoria, "value": float(row.valor_liquido)}
                       for row in by_category.itertuples()],
        "cities": [{"name": row.cidade, "value": float(row.valor_liquido)}
                   for row in by_city.itertuples()],
        "rows": [{**row, "data": row["data"][:10]}
                 for row in records(table[columns])],
        "total_rows": len(df),
    }


@app.get("/api/advanced/{dataset_id}")
def advanced(
    dataset_id: str, analysis: str,
    start: date | None = None, end: date | None = None,
    cities: list[str] = Query(default=[]), categories: list[str] = Query(default=[]),
    days: int = Query(default=15, ge=1, le=60),
) -> dict:
    df = filtered(dataset_id, start, end, cities, categories)
    if df.empty:
        return {"status": "empty"}
    if analysis == "rfm":
        return {"status": "ok", "rows": records(calcular_rfm(df))}
    if analysis == "forecast":
        if df["data"].nunique() < 2:
            return {"status": "insufficient"}
        trend, model = treinar_regressao_faturamento(df)
        target = pd.DataFrame({"dias_corridos": [trend["dias_corridos"].max() + days]})
        return {
            "status": "ok",
            "estimate": max(0, float(model.predict(target)[0])),
            "rows": [{"date": row.data.date().isoformat(), "actual": float(row.valor_liquido),
                      "trend": float(row.tendencia_prevista)} for row in trend.itertuples()],
        }
    if analysis == "correlation":
        cols = ["quantidade", "preco_unitario", "desconto", "avaliacao", "valor_liquido"]
        corr = df[cols].corr().round(2)
        return {
            "status": "ok", "columns": cols,
            "matrix": corr.astype(object).where(pd.notna(corr), None).values.tolist(),
            "points": [{"category": row.categoria, "value": float(row.valor_liquido)}
                       for row in df.itertuples()],
        }
    if analysis == "3d":
        points = df.iloc[:1000]
        cols = ["produto", "cidade", "categoria", "quantidade", "preco_unitario",
                "avaliacao", "valor_liquido"]
        return {"status": "ok", "total": len(df), "points": records(points[cols])}
    raise HTTPException(422, "Análise desconhecida.")
