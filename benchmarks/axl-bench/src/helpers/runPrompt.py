import os
from typing import Dict, List

from anthropic import Anthropic
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

from ..models import ClaudeModel, GeminiModel, OpenAiModel
from .anthropic import runPrompt as anthropicRunPrompt
from .gemini import runPrompt as geminiRunPrompt
from .openai import runPrompt as openaiRunPrompt

load_dotenv()


def runPrompt(
    model: str,
    maxTokens: int,
    temperature: float,
    messages: List[Dict[str, str]],
    enableGrounding: bool = False,
) -> str:
    """
    Gateway function to run a prompt through the appropriate LLM API.

    This function automatically detects the provider based on the model name
    and routes to the correct implementation (Anthropic, OpenAI, or Gemini).

    Args:
        model: The model identifier
        maxTokens: Maximum number of tokens to generate
        temperature: Temperature for sampling (0.0 to 1.0)
        messages: List of message dictionaries with 'role' and 'content' keys
        enableGrounding: Whether to enable web search/grounding (default: False)

    Returns:
        The generated text response from the model

    Raises:
        ValueError: If the model provider cannot be determined
    """
    # Detect provider based on model name
    if any(model == member.value for member in ClaudeModel):
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        return anthropicRunPrompt(
            client, model, maxTokens, temperature, messages, enableGrounding
        )

    elif any(model == member.value for member in OpenAiModel):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        return openaiRunPrompt(
            client, model, maxTokens, temperature, messages, enableGrounding
        )

    elif any(model == member.value for member in GeminiModel):
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        return geminiRunPrompt(
            client, model, maxTokens, temperature, messages, enableGrounding
        )

    else:
        raise ValueError(
            f"Unable to determine provider for model: {model}. Model must be registered in ClaudeModel, OpenAiModel, or GeminiModel enums. Available models: {ClaudeModel}, {OpenAiModel}, {GeminiModel}"  # noqa: E501
        )
