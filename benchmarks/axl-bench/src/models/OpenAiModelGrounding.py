from enum import Enum


class OpenAiModelGrounding(Enum):
    """
    Enum of OpenAI models that support web_search tool via Responses API.
    Source: https://platform.openai.com/docs/api-reference/responses
    """

    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    O3 = "o3"
    O4_MINI = "o4-mini"
    GPT_5 = "gpt-5"
