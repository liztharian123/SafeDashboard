from sqlalchemy.ext.asyncio import AsyncSession

from app.mappers.dashboard_mapper import get_dashboard_summary, get_recent_transactions
from app.schemas.dashboard import DashboardDataResponse


async def get_dashboard_data(session: AsyncSession) -> DashboardDataResponse:
    summary = await get_dashboard_summary(session)
    recent_transactions = await get_recent_transactions(session, limit=50)
    return DashboardDataResponse(
        summary=summary,
        recent_transactions=recent_transactions,
    )
