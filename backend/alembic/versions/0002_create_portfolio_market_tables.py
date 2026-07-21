"""create portfolio and market tables (portfolios, assets, transactions, asset_price_history, benchmark_history)

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-21

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "portfolios",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False, server_default="Carteira Principal"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "assets",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("ticker", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("asset_class", sa.String(length=20), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="BRL"),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.CheckConstraint(
            "asset_class IN ('acao', 'fii', 'etf', 'tesouro_direto')", name="ck_asset_class"
        ),
    )
    op.create_index("ix_assets_ticker", "assets", ["ticker"], unique=True)

    op.create_table(
        "transactions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("portfolio_id", sa.Uuid(), sa.ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("asset_id", sa.Uuid(), sa.ForeignKey("assets.id"), nullable=False),
        sa.Column("operation", sa.String(length=10), nullable=False),
        sa.Column("quantity", sa.Numeric(18, 8), nullable=False),
        sa.Column("unit_price", sa.Numeric(18, 6), nullable=False),
        sa.Column("fees", sa.Numeric(18, 6), nullable=False, server_default="0"),
        sa.Column("operation_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("operation IN ('compra', 'venda')", name="ck_transaction_operation"),
    )

    op.create_table(
        "asset_price_history",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("asset_id", sa.Uuid(), sa.ForeignKey("assets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("price_date", sa.Date(), nullable=False),
        sa.Column("close_price", sa.Numeric(18, 6), nullable=False),
        sa.Column("volume", sa.Numeric(20, 2), nullable=True),
        sa.UniqueConstraint("asset_id", "price_date", name="uq_asset_price_history_asset_date"),
    )

    op.create_table(
        "benchmark_history",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("benchmark_code", sa.String(length=10), nullable=False),
        sa.Column("ref_date", sa.Date(), nullable=False),
        sa.Column("value", sa.Numeric(18, 8), nullable=False),
        sa.UniqueConstraint("benchmark_code", "ref_date", name="uq_benchmark_history_code_date"),
        sa.CheckConstraint("benchmark_code IN ('cdi', 'ipca', 'ibov')", name="ck_benchmark_code"),
    )


def downgrade() -> None:
    op.drop_table("benchmark_history")
    op.drop_table("asset_price_history")
    op.drop_table("transactions")
    op.drop_index("ix_assets_ticker", table_name="assets")
    op.drop_table("assets")
    op.drop_table("portfolios")
