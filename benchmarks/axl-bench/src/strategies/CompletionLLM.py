from typing import Optional, Union

from axelrod import Action, Player
from dotenv import load_dotenv

from ..helpers import runPrompt
from ..models import (
    ClaudeModel,
    ClaudeModelGrounding,
    GeminiModel,
    GeminiModelGrounding,
    Message,
    OpenAiModel,
    OpenAiModelGrounding,
    PromptContext,
)

load_dotenv()


class CompletionLLM(Player):
    """
    A LLM player that can be used in an Axelrod tournament.
    """

    def __init__(
        self,
        # Axelrod parameters
        name: str = "CompletionLLM",
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
        # Model parameters
        model: Union[
            ClaudeModel,
            OpenAiModel,
            GeminiModel,
            ClaudeModelGrounding,
            OpenAiModelGrounding,
            GeminiModelGrounding,
        ] = GeminiModel.GEMINI_2_5_FLASH_LITE,
        maxTokens: int = 1024,
        temperature: float = 1.0,
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
        # Model parameters
        self.model: Union[
            ClaudeModel,
            OpenAiModel,
            GeminiModel,
            ClaudeModelGrounding,
            OpenAiModelGrounding,
            GeminiModelGrounding,
        ] = model
        self.maxTokens: int = maxTokens
        self.temperature: float = temperature

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
        move: str = runPrompt(
            model=self.model.value,
            maxTokens=self.maxTokens,
            temperature=self.temperature,
            messages=[
                Message(role="user", content=self.promptContext.formatPrompt()),
            ],
        )

        if move == "C":
            return Action.C
        elif move == "D":
            return Action.D
        else:
            raise ValueError(f"Invalid move: {move}")
