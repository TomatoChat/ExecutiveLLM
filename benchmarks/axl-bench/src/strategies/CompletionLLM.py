import os
from typing import Optional, Union

from anthropic import Anthropic
from axelrod import Action, Player
from dotenv import load_dotenv

from ..models import ClaudeModel, PromptContext

load_dotenv()


class CompletionLLM(Player):
    """
    A LLM player that can be used in an Axelrod tournament.
    """

    def __init__(
        self,
        # Axelrod parameters
        name: Optional[str] = "OpenAI",
        memoryDepth: Optional[Union[int, float]] = float("inf"),
        stochastic: Optional[bool] = True,
        inspectsSource: Optional[bool] = False,
        manipulatesSource: Optional[bool] = False,
        manipulatesState: Optional[bool] = False,
        # Prompt parameters
        promptTemplate: str = "",
        historyLastTurns: Optional[int] = None,
        numTurns: Optional[int] = None,
        endProbability: Optional[float] = None,
        # Anthropic parameters
        apiKey: Optional[str] = None,
        model: Optional[ClaudeModel] = ClaudeModel.CLAUDE_3_7_SONNET_20250219,
        maxTokens: Optional[int] = 1024,
        temperature: Optional[float] = 1.0,
    ):
        super().__init__()

        # Axelrod parameters
        self.name: str = name
        self.classifier = {
            "memory_depth": memoryDepth,
            "stochastic": stochastic,
            "inspects_source": inspectsSource,
            "manipulates_source": manipulatesSource,
            "manipulates_state": manipulatesState,
        }
        # Prompt parameters
        self.promptTemplate: str = promptTemplate
        self.historyLastTurns: Optional[int] = historyLastTurns
        self.numTurns: Optional[int] = numTurns
        self.endProbability: Optional[float] = endProbability
        # Anthropic parameters
        self.apiKey: str = (
            apiKey if apiKey is not None else os.getenv("ANTHROPIC_API_KEY")
        )
        self.model: ClaudeModel = model
        self.maxTokens: int = maxTokens
        self.temperature: float = temperature
        self.client = Anthropic(api_key=self.apiKey)

    def __repr__(self) -> str:
        return self.name

    def strategy(self, opponent: Player) -> Action:
        """
        Run the prompt and return the action.

        Args:
            opponent: The opponent player

        Returns:
            The action to take
        """

        self.promptContext = PromptContext(
            promptTemplate=self.promptTemplate,
            personalHistory=self.history,
            opponentHistory=opponent.history,
            historyLastTurns=self.historyLastTurns,
            numTurns=self.numTurns,
            endProbability=self.endProbability,
        )
        move: str = self._runPrompt()

        if move == "C":
            return Action.C
        elif move == "D":
            return Action.D
        else:
            raise ValueError(f"Invalid move: {move}")

    def _runPrompt(self) -> str:
        """
        Format the prompt and send it to Claude API for completion.

        Returns:
            The text response from Claude
        """

        response = self.client.messages.create(
            model=self.model.value,
            max_tokens=self.maxTokens,
            messages=[
                {"role": "user", "content": self.promptContext.formatPrompt()},
            ],
        )

        return response.content[0].text
