import os
from typing import List

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


def getModelIds() -> List[str]:
    """
    Retrieve just the model IDs from the Anthropic API.

    Returns:
        List of model ID strings
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    page = client.models.list()

    return [model.id for model in page.data]
