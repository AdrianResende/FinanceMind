from fastapi import APIRouter

from app.api.v1 import auth, health, market, portfolio, transactions, users

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(market.router)
api_router.include_router(portfolio.router)
api_router.include_router(transactions.router)
