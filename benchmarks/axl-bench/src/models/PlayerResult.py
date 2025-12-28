"""
Model for individual player results.
"""

from pydantic import BaseModel


class PlayerResult(BaseModel):
    """Results for a single player in the tournament."""

    name: str
    score: float
    rank: int
    wins: int
    cooperationRate: float
