import logging
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

import httpx

from app.core.config import get_settings

logger = logging.getLogger("financemind.brapi")
settings = get_settings()


@dataclass
class BrapiQuote:
    ticker: str
    name: str
    price: Decimal
    currency: str


@dataclass
class BrapiHistoryPoint:
    price_date: date
    close_price: Decimal
    volume: Decimal | None


def _auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {settings.brapi_token}"}


async def get_quotes(tickers: list[str]) -> list[BrapiQuote]:
    if not settings.brapi_token:
        logger.warning("BRAPI_TOKEN não configurado — sync de cotações ignorado.")
        return []
    if not tickers:
        return []

    url = f"{settings.brapi_base_url}/quote/{','.join(tickers)}"
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url, headers=_auth_headers())
        response.raise_for_status()
        data = response.json()

    quotes: list[BrapiQuote] = []
    for item in data.get("results", []):
        price = item.get("regularMarketPrice")
        if price is None:
            continue
        quotes.append(
            BrapiQuote(
                ticker=item["symbol"],
                name=item.get("longName") or item.get("shortName") or item["symbol"],
                price=Decimal(str(price)),
                currency=item.get("currency", "BRL"),
            )
        )
    return quotes


async def get_history(ticker: str, range_: str = "1y", interval: str = "1d") -> list[BrapiHistoryPoint]:
    if not settings.brapi_token:
        logger.warning("BRAPI_TOKEN não configurado — histórico de %s ignorado.", ticker)
        return []

    url = f"{settings.brapi_base_url}/quote/{ticker}"
    params = {"range": range_, "interval": interval}
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url, headers=_auth_headers(), params=params)
        response.raise_for_status()
        data = response.json()

    results = data.get("results", [])
    if not results:
        return []

    points: list[BrapiHistoryPoint] = []
    for row in results[0].get("historicalDataPrice", []):
        close = row.get("close")
        if close is None:
            continue
        row_date = datetime.fromtimestamp(row["date"]).date() if isinstance(row.get("date"), int) else None
        if row_date is None:
            continue
        volume = row.get("volume")
        points.append(
            BrapiHistoryPoint(
                price_date=row_date,
                close_price=Decimal(str(close)),
                volume=Decimal(str(volume)) if volume is not None else None,
            )
        )
    return points
