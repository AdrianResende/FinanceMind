import csv
import io
import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation

import httpx

logger = logging.getLogger("financemind.tesouro")

CSV_URL = (
    "https://www.tesourotransparente.gov.br/ckan/dataset/"
    "df56aa42-484a-4a59-8184-7676580c81e3/resource/"
    "796d2059-14e9-44e3-80c9-2d9e30b405c1/download/precotaxatesourodireto.csv"
)

HISTORY_WINDOW_DAYS = 2 * 365


@dataclass
class TesouroRow:
    titulo: str
    vencimento: date
    data_base: date
    pu_base: Decimal


def _parse_decimal(raw: str) -> Decimal | None:
    if not raw:
        return None
    try:
        return Decimal(raw.strip().replace(",", "."))
    except InvalidOperation:
        return None


def _parse_date(raw: str) -> date | None:
    if not raw:
        return None
    try:
        return datetime.strptime(raw.strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


async def fetch_tesouro_prices() -> list[TesouroRow]:
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(CSV_URL)
        response.raise_for_status()
        content = response.content.decode("latin-1")

    cutoff = date.today() - timedelta(days=HISTORY_WINDOW_DAYS)
    rows: list[TesouroRow] = []
    reader = csv.DictReader(io.StringIO(content), delimiter=";")
    for record in reader:
        data_base = _parse_date(record.get("Data Base", ""))
        if data_base is None or data_base < cutoff:
            continue

        vencimento = _parse_date(record.get("Data Vencimento", ""))
        pu_base = _parse_decimal(record.get("PU Base Manha", ""))
        titulo = record.get("Tipo Titulo", "").strip()
        if vencimento is None or pu_base is None or not titulo:
            continue

        rows.append(TesouroRow(titulo=titulo, vencimento=vencimento, data_base=data_base, pu_base=pu_base))

    return rows
