from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.jobs.market_sync_job import run_market_sync

scheduler = AsyncIOScheduler()


def configure_scheduler() -> AsyncIOScheduler:
    if not scheduler.get_job("market_sync"):
        scheduler.add_job(run_market_sync, "cron", hour=6, minute=0, id="market_sync")
    return scheduler
