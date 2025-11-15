from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.stats_schema import StatsResponse
from app.services.stats_service import StatsService

stats_router = APIRouter()


@stats_router.get("/stats", response_model=StatsResponse)
async def get_stats(session: AsyncSession = Depends(get_session)):
    data = await StatsService.get_stats(session)
    return StatsResponse(**data)
