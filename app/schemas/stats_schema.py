from typing import Dict

from pydantic import BaseModel


class StatsResponse(BaseModel):
    total_pr: int
    open_pr: int
    merged_pr: int
    total_assignments: int
    assignments_by_user: Dict[str, int]
    pr_by_author: Dict[str, int]
