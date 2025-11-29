import os
from enum import Enum
from typing import List

from anthropic import Anthropic
from anthropic.types import ModelInfo
from dotenv import load_dotenv


def getAnthropicModels() -> List[ModelInfo]:
    """
    Retrieve the list of available Anthropic models from the API.

    Returns:
        List of ModelInfo objects containing model information
    """
    load_dotenv()
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    page = client.models.list()

    return page.data


def getModelIds() -> List[str]:
    """
    Retrieve just the model IDs from the Anthropic API.

    Returns:
        List of model ID strings
    """
    models = getAnthropicModels()

    return [model.id for model in models]


def _modelIdToEnumName(modelId: str) -> str:
    """
    Convert a model ID to a valid Python enum name.

    Args:
        model_id: The model ID string (e.g., "claude-3-5-sonnet-20241022")

    Returns:
        Valid enum name (e.g., "CLAUDE_3_5_SONNET_20241022")
    """
    return modelId.upper().replace("-", "_").replace(".", "_")


modelIds = getModelIds()
enumsDict = {_modelIdToEnumName(modelId): modelId for modelId in modelIds}
ClaudeModel = Enum("ClaudeModel", enumsDict)
