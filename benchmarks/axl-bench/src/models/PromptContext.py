from typing import List, Optional

from axelrod.action import Action
from pydantic import BaseModel


class PromptContext(BaseModel):
    promptTemplate: str
    personalHistory: List[Action] = []
    opponentHistory: List[Action] = []
    historyLastTurns: Optional[int] = None
    numTurns: Optional[int] = None
    endProbability: Optional[float] = None

    def formatPrompt(self) -> str:
        """
        Format a prompt template with the context variables.

        If numTurnsLastTurns is set, only the last N turns of history are used.
        Otherwise, the full history is used.

        Args:
            promptTemplate: A string containing placeholders like {numTurns}, {history}, etc.

        Returns:
            The formatted prompt string
        """
        variables: dict[str, str] = {}
        personalHistory: List[Action] = (
            self.personalHistory
            if self.historyLastTurns is None
            else self.personalHistory[-self.historyLastTurns :]
        )
        opponentHistory: List[Action] = (
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
