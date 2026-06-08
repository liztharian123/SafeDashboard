from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.dashboard import DashboardDataResponse
from app.services.dashboard_service import get_dashboard_data

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    data = await get_dashboard_data(session)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "summary": data.summary,
        },
    )


@router.get("/api/dashboard/data", response_model=DashboardDataResponse)
async def dashboard_data_api(session: AsyncSession = Depends(get_db)):
    return await get_dashboard_data(session)
