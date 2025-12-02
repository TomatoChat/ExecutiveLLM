from enum import Enum


class ClaudeModelGrounding(Enum):
    """
    Enum of Claude models that support web search.
    Source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool
    """

    CLAUDE_SONNET_4_5 = "claude-sonnet-4-5"
    CLAUDE_SONNET_4 = "claude-sonnet-4"
    CLAUDE_HAIKU_4_5 = "claude-haiku-4-5"
    CLAUDE_HAIKU_3_5 = "claude-haiku-3-5"
    CLAUDE_OPUS_4_5 = "claude-opus-4-5"
    CLAUDE_OPUS_4_1 = "claude-opus-4-1"
    CLAUDE_OPUS_4 = "claude-opus-4"
