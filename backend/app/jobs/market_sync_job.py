import logging

from app.db.session import AsyncSessionLocal
from app.services import market_sync_service

logger = logging.getLogger("financemind.market_sync")


async def run_market_sync() -> None:
    async with AsyncSessionLocal() as db:
        for label, sync_fn in (
            ("ações/FIIs/ETFs", market_sync_service.sync_stocks_and_funds),
            ("tesouro direto", market_sync_service.sync_tesouro_direto),
            ("benchmarks (CDI/IPCA)", market_sync_service.sync_benchmarks),
            ("benchmark IBOV", market_sync_service.sync_ibov_benchmark),
        ):
            try:
                count = await sync_fn(db)
                logger.info("Sync de %s concluído: %d registros.", label, count)
            except Exception:
                logger.exception("Falha ao sincronizar %s.", label)
