from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: str
    amount: Decimal
    currency: str
    type: str
    status: str
    description: str | None
    created_at: datetime


class DashboardSummary(BaseModel):
    total_transactions: int
    total_credits: Decimal
    total_debits: Decimal
    pending_count: int
    failed_count: int


class DashboardDataResponse(BaseModel):
    summary: DashboardSummary
    recent_transactions: list[TransactionOut]
