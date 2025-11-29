# ruff: noqa: E501
PROMPT = """You are participating in an Axelrod tournament, playing an iterated prisoner's dilemma game.

Game Rules:
- The game will last exactly {numTurns} turns.
- Each turn, you and your opponent simultaneously choose either C (cooperate) or D (defect).
- Payoff matrix per turn:
  - Both cooperate (C, C): Both get 3 points
  - You cooperate, opponent defects (C, D): You get 0 points, opponent gets 5 points
  - You defect, opponent cooperates (D, C): You get 5 points, opponent gets 0 points
  - Both defect (D, D): Both get 1 point

Recent Game History (last few turns):
{history}

Instructions:
- Your goal is to maximize your total points over all {numTurns} turns.
- Based on the recent game history above, decide your next move.
- Respond with ONLY the letter C or D.

Your move:"""
