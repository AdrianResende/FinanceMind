"""create dividend_receipts table

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-21

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dividend_receipts",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("portfolio_id", sa.Uuid(), sa.ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("asset_id", sa.Uuid(), sa.ForeignKey("assets.id"), nullable=False),
        sa.Column("amount", sa.Numeric(18, 6), nullable=False),
        sa.Column("payment_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("dividend_receipts")
