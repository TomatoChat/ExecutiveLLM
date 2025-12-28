from typing import Dict, Optional

from axelrod import History
from pydantic import BaseModel, ConfigDict, Field


class PromptContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    promptTemplate: str
    personalHistory: History = Field(default_factory=History)
    opponentHistory: History = Field(default_factory=History)
    historyLastTurns: Optional[int] = None
    numTurns: Optional[int] = None
    endProbability: Optional[float] = None

    def formatPrompt(self) -> str:
        """
        Format a prompt template with the context variables.

        If numTurnsLastTurns is set, only the last N turns of history are used.
        Otherwise, the full history is used.

        Args:
            promptTemplate: A string containing placeholders

        Returns:
            The formatted prompt string
        """
        variables: Dict[str, str] = {}
        personalHistory: History = (
            self.personalHistory
            if self.historyLastTurns is None
            else self.personalHistory[-self.historyLastTurns :]
        )
        opponentHistory: History = (
            self.opponentHistory
            if self.historyLastTurns is None
            else self.opponentHistory[-self.historyLastTurns :]
        )

        if self.numTurns is not None:
            variables["numTurns"] = str(self.numTurns)

        if self.endProbability is not None:
            variables["endProbability"] = str(self.endProbability)

        variables["personalHistory"] = "".join(
            [action.name for action in personalHistory]
        )
        variables["opponentHistory"] = "".join(
            [action.name for action in opponentHistory]
        )

        return self.promptTemplate.format(**variables)
