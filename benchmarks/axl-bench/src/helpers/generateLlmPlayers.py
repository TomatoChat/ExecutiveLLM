"""
Helper function to generate all LLM players for benchmarking.
"""

from typing import List

import axelrod as axl

from ..models import (
    ClaudeModel,
    ClaudeModelGrounding,
    GeminiModel,
    GeminiModelGrounding,
    OpenAiModel,
    OpenAiModelGrounding,
    PromptConfig,
)
from ..prompts.contextualized import (
    STRATEGY_PREDETERMINED_TURNS_FULL_HISTORY,
    STRATEGY_PREDETERMINED_TURNS_LAST_TURNS,
    STRATEGY_PROBABILISTIC_END_FULL_HISTORY,
    STRATEGY_PROBABILISTIC_END_LAST_TURNS,
)
from ..prompts.uncontextualized import STRATEGY_FULL_HISTORY, STRATEGY_LAST_TURNS
from ..strategies import CompletionLLM


def generateLlmPlayers(
    numTurns: int,
    includeRegular: bool = True,
    includeGrounding: bool = True,
    maxTokens: int = 1024,
    temperature: float = 1.0,
) -> List[axl.Player]:
    """
    Generates all LLM players for the benchmark.

    Creates players for all combinations of:
    - Regular models (Claude, OpenAI, Gemini)
    - Grounding-enabled models (with web search capability)
    - All available prompt templates (6 total)

    Args:
        numTurns: Number of turns in the tournament (used for contextualized prompts)
        includeRegular: Whether to include regular (non-grounding) models
        includeGrounding: Whether to include grounding-enabled models
        maxTokens: Maximum tokens for LLM responses
        temperature: Temperature parameter for LLM

    Returns:
        List of all CompletionLLM players
    """
    players: List[axl.Player] = []
    promptConfigs: List[PromptConfig] = [
        PromptConfig(
            template=STRATEGY_FULL_HISTORY,
            nameSuffix="FullHist",
        ),
        PromptConfig(
            template=STRATEGY_LAST_TURNS,
            nameSuffix="LastTurns",
            historyLastTurns=5,
        ),
        PromptConfig(
            template=STRATEGY_PREDETERMINED_TURNS_FULL_HISTORY,
            nameSuffix="PredetFullHist",
            numTurns=numTurns,
        ),
        PromptConfig(
            template=STRATEGY_PREDETERMINED_TURNS_LAST_TURNS,
            nameSuffix="PredetLastTurns",
            historyLastTurns=5,
            numTurns=numTurns,
        ),
        # Contextualized prompts - probabilistic end
        PromptConfig(
            template=STRATEGY_PROBABILISTIC_END_FULL_HISTORY,
            nameSuffix="ProbEndFullHist",
            endProbability=10.0,  # 10% chance of ending each turn
        ),
        PromptConfig(
            template=STRATEGY_PROBABILISTIC_END_LAST_TURNS,
            nameSuffix="ProbEndLastTurns",
            historyLastTurns=5,
            endProbability=10.0,  # 10% chance of ending each turn
        ),
    ]

    if includeRegular:
        # Claude models
        for model in ClaudeModel:
            for config in promptConfigs:
                players.append(
                    CompletionLLM(
                        name=f"{model.name}_{config.nameSuffix}",
                        promptTemplate=config.template,
                        historyLastTurns=config.historyLastTurns,
                        numTurns=config.numTurns,
                        endProbability=config.endProbability,
                        model=model,
                        maxTokens=maxTokens,
                        temperature=temperature,
                    )
                )

        # OpenAI models
        for model in OpenAiModel:
            for config in promptConfigs:
                players.append(
                    CompletionLLM(
                        name=f"{model.name}_{config.nameSuffix}",
                        promptTemplate=config.template,
                        historyLastTurns=config.historyLastTurns,
                        numTurns=config.numTurns,
                        endProbability=config.endProbability,
                        model=model,
                        maxTokens=maxTokens,
                        temperature=temperature,
                    )
                )

        # Gemini models
        for model in GeminiModel:
            for config in promptConfigs:
                players.append(
                    CompletionLLM(
                        name=f"{model.name}_{config.nameSuffix}",
                        promptTemplate=config.template,
                        historyLastTurns=config.historyLastTurns,
                        numTurns=config.numTurns,
                        endProbability=config.endProbability,
                        model=model,
                        maxTokens=maxTokens,
                        temperature=temperature,
                    )
                )

    if includeGrounding:
        # Claude grounding models
        for model in ClaudeModelGrounding:
            for config in promptConfigs:
                players.append(
                    CompletionLLM(
                        name=f"{model.name}_GROUNDING_{config.nameSuffix}",
                        promptTemplate=config.template,
                        historyLastTurns=config.historyLastTurns,
                        numTurns=config.numTurns,
                        endProbability=config.endProbability,
                        model=model,
                        maxTokens=maxTokens,
                        temperature=temperature,
                    )
                )

        # OpenAI grounding models
        for model in OpenAiModelGrounding:
            for config in promptConfigs:
                players.append(
                    CompletionLLM(
                        name=f"{model.name}_GROUNDING_{config.nameSuffix}",
                        promptTemplate=config.template,
                        historyLastTurns=config.historyLastTurns,
                        numTurns=config.numTurns,
                        endProbability=config.endProbability,
                        model=model,
                        maxTokens=maxTokens,
                        temperature=temperature,
                    )
                )

        # Gemini grounding models
        for model in GeminiModelGrounding:
            for config in promptConfigs:
                players.append(
                    CompletionLLM(
                        name=f"{model.name}_GROUNDING_{config.nameSuffix}",
                        promptTemplate=config.template,
                        historyLastTurns=config.historyLastTurns,
                        numTurns=config.numTurns,
                        endProbability=config.endProbability,
                        model=model,
                        maxTokens=maxTokens,
                        temperature=temperature,
                    )
                )

    return players
