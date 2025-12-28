"""
Model for tournament score statistics.
"""

from pydantic import BaseModel


class ScoreStatistics(BaseModel):
    """Statistics about scores in the tournament."""

    mean: float
    median: float
    std: float
    min: float
    max: float
