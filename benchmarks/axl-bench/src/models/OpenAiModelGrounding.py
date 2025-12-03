from enum import Enum


class OpenAiModelGrounding(Enum):
    """
    Enum of OpenAI models that support web search.
    Source: OpenAI documentation and community forums
    Note: Web search is only supported on specific models like GPT-4.1 series,
    GPT-5 search variants, and search-optimized models.
    """

    # GPT-4.1 series (supports web search)
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_PREVIEW = "gpt-4.1-preview"
    GPT_4O_SEARCH_PREVIEW = "gpt-4o-search-preview"
    GPT_4O_MINI_SEARCH_PREVIEW = "gpt-4o-mini-search-preview"
    GPT_5_SEARCH_API = "gpt-5-search-api"
    GPT_5_SEARCH_API_2025_10_14 = "gpt-5-search-api-2025-10-14"
