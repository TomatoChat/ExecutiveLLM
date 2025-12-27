from enum import Enum


class ClaudeModel(Enum):
    """
    Enum of available Claude models.
    """

    CLAUDE_OPUS_4_5_20251101 = "claude-opus-4-5-20251101"
    CLAUDE_SONNET_4_5_20250929 = "claude-sonnet-4-5-20250929"
    CLAUDE_3_7_SONNET_20250219 = "claude-3-7-sonnet-20250219"
    CLAUDE_3_5_SONNET_20241022 = "claude-3-5-sonnet-20241022"
    CLAUDE_3_5_SONNET_20240620 = "claude-3-5-sonnet-20240620"
    CLAUDE_3_OPUS_20240229 = "claude-3-opus-20240229"
    CLAUDE_3_SONNET_20240229 = "claude-3-sonnet-20240229"
    CLAUDE_3_HAIKU_20240307 = "claude-3-haiku-20240307"
