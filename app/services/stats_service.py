from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.stats_repository import StatsRepository


class StatsService:
    @staticmethod
    async def get_stats(session: AsyncSession):
        return await StatsRepository.get_stats(session)
