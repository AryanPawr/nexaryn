from typing import Any

from app.schemas.common import NexarynSchema


class PostureScoreResponse(NexarynSchema):
    overall_score: int
    trend: str
    summary_counts: dict[str, Any]
    drivers: list[str]
