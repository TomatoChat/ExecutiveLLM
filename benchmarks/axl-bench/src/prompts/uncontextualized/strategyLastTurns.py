# ruff: noqa: E501
PROMPT = """You are playing a game with another player.

Game Rules:
- Each round, you and the other player simultaneously choose either C or D.
- Scoring per round:
  - Both choose C: Both get 3 points
  - You choose C, other chooses D: You get 0 points, other gets 5 points
  - You choose D, other chooses C: You get 5 points, other gets 0 points
  - Both choose D: Both get 1 point

Recent Game History (last few rounds):
Your moves:  {personalHistory}
Other moves: {opponentHistory}

Instructions:
- Your goal is to maximize your total points.
- Based on the recent game history above, decide your next move.
- Respond with ONLY the letter C or D.

Your move:"""
