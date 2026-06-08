from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction
from app.schemas.dashboard import DashboardSummary, TransactionOut


async def get_recent_transactions(
    session: AsyncSession, limit: int = 50
) -> list[TransactionOut]:
    result = await session.execute(
        select(Transaction).order_by(Transaction.created_at.desc()).limit(limit)
    )
    rows = result.scalars().all()
    return [TransactionOut.model_validate(row) for row in rows]


async def get_dashboard_summary(session: AsyncSession) -> DashboardSummary:
    total = await session.execute(select(func.count(Transaction.id)))
    total_count = total.scalar_one()

    credits = await session.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.type == "credit"
        )
    )
    total_credits = credits.scalar_one()

    debits = await session.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.type == "debit"
        )
    )
    total_debits = debits.scalar_one()

    pending = await session.execute(
        select(func.count(Transaction.id)).where(Transaction.status == "pending")
    )
    pending_count = pending.scalar_one()

    failed = await session.execute(
        select(func.count(Transaction.id)).where(Transaction.status == "failed")
    )
    failed_count = failed.scalar_one()

    return DashboardSummary(
        total_transactions=total_count,
        total_credits=Decimal(str(total_credits)),
        total_debits=Decimal(str(total_debits)),
        pending_count=pending_count,
        failed_count=failed_count,
    )
