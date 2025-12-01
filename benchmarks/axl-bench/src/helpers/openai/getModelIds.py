import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def getModelIds() -> List[str]:
    """
    Retrieve just the model IDs from the OpenAI API.

    Returns:
        List of model ID strings
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    models = client.models.list()

    return [model.id for model in models.data]
