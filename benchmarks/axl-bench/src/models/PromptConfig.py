"""
Model for prompt configuration.
"""

from typing import Optional

from pydantic import BaseModel


class PromptConfig(BaseModel):
    """Configuration for a prompt template."""

    template: str
    nameSuffix: str
    historyLastTurns: Optional[int] = None
    numTurns: Optional[int] = None
    endProbability: Optional[float] = None
