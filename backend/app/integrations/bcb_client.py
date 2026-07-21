from datetime import date, datetime
from decimal import Decimal

import httpx

SGS_BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"

SGS_CODE_CDI = 12
SGS_CODE_IPCA = 433


async def get_sgs_series(codigo: int, data_inicial: date, data_final: date) -> list[tuple[date, Decimal]]:
    url = SGS_BASE_URL.format(codigo=codigo)
    params = {
        "formato": "json",
        "dataInicial": data_inicial.strftime("%d/%m/%Y"),
        "dataFinal": data_final.strftime("%d/%m/%Y"),
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    series: list[tuple[date, Decimal]] = []
    for row in data:
        row_date = datetime.strptime(row["data"], "%d/%m/%Y").date()
        value = Decimal(row["valor"].replace(",", "."))
        series.append((row_date, value))
    return series
