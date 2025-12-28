"""
Model for tournament iteration results.
"""

from typing import List, Optional

from pydantic import BaseModel

from .PlayerResult import PlayerResult
from .ScoreStatistics import ScoreStatistics


class TournamentIterationResult(BaseModel):
    """Results from a single tournament iteration."""

    iteration: int
    timestamp: str
    durationSeconds: float
    turns: int
    seed: int
    numPlayers: int
    playerNames: List[str]
    scores: List[float]
    rankedNames: List[str]
    wins: List[int]
    matchLengths: List[List[int]]
    cooperationRates: List[float]
    payoffMatrix: List[List[float]]
    scoreStatistics: ScoreStatistics
    playerResults: List[PlayerResult]
    error: Optional[str] = None
