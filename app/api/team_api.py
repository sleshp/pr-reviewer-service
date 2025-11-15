from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.requests_schema import TeamCreateRequest
from app.schemas.team_schema import Team, TeamResponse
from app.services.team_service import TeamService

router = APIRouter()


@router.post("/add", response_model=TeamResponse, status_code=201)
async def add_team(
    data: TeamCreateRequest,
    session: AsyncSession = Depends(get_session),
):
    team = await TeamService.create_team(
        session=session,
        team_name=data.team_name,
        members=data.members,
    )
    return TeamResponse(team=team)


@router.get("/get", response_model=TeamResponse)
async def get_team(
    team_name: str,
    session: AsyncSession = Depends(get_session),
):
    team = await TeamService.get_team(session, team_name)
    return TeamResponse(team=team)
