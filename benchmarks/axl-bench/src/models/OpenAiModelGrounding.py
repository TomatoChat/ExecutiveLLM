from enum import Enum


class OpenAiModelGrounding(Enum):
    """
    Enum of OpenAI models that support web search.
    Source: OpenAI documentation and community forums
    """

    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_1 = "gpt-4.1"
    O1 = "o1"
    O3 = "o3"
