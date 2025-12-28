"""
Model for benchmark metadata.
"""

from pydantic import BaseModel


class BenchmarkMetadata(BaseModel):
    """Metadata about the benchmark run."""

    benchmarkDate: str
    iterations: int
    turnsPerMatch: int
    baseSeed: int
    totalPlayers: int
    numAxelrodStrategies: int
    numLlmPlayers: int
    includeRegularModels: bool
    includeGroundingModels: bool
    maxTokens: int
    temperature: float
