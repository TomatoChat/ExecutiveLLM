"""
Helper function to run a single tournament iteration.
"""

import time
from typing import List, cast

import axelrod as axl
import numpy as np

from ..models import PlayerResult, ScoreStatistics, TournamentIterationResult


def runTournamentIteration(
    players: List[axl.Player],
    iterationNumber: int,
    turns: int = 200,
    seed: int = 42,
) -> TournamentIterationResult:
    """
    Runs a single tournament iteration with the given players.
    """
    print(f"\n=== Running Tournament Iteration {iterationNumber} ===")
    print(f"Players: {len(players)}")
    print(f"Turns: {turns}")
    print(f"Seed: {seed}")

    startTime: float = time.time()

    tournament: axl.Tournament = axl.Tournament(
        players=players,
        turns=turns,
        seed=seed,
        repetitions=1,
    )
    results: axl.ResultSet = tournament.play(processes=1)

    endTime: float = time.time()
    duration: float = endTime - startTime

    playerNames: List[str] = [str(player) for player in players]

    scores: List[List[float]] = results.scores
    rankedNames: List[str] = results.ranked_names
    wins: List[int] = cast(List[int], results.wins)
    matchLengths: List[List[int]] = results.match_lengths
    payoffMatrix: List[List[int]] = results.payoff_matrix

    cooperationRates: List[float] = []

    for i, _ in enumerate(players):
        totalMoves = 0
        cooperations = 0

        for match in results.interactions:
            for interaction in match:
                if i in interaction:
                    moves = interaction[i]
                    totalMoves += len(moves)
                    cooperations += sum(1 for move in moves if move == axl.Action.C)

        cooperationRate = cooperations / totalMoves if totalMoves > 0 else 0.0
        cooperationRates.append(cooperationRate)

    playerScores: List[float] = [float(np.mean(row)) for row in scores]

    scoreStats = ScoreStatistics(
        mean=float(np.mean(playerScores)),
        median=float(np.median(playerScores)),
        std=float(np.std(playerScores)),
        min=float(np.min(playerScores)),
        max=float(np.max(playerScores)),
    )

    iterationResults = TournamentIterationResult(
        iteration=iterationNumber,
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        durationSeconds=duration,
        turns=turns,
        seed=seed,
        numPlayers=len(players),
        playerNames=playerNames,
        scores=playerScores,
        rankedNames=rankedNames,
        wins=wins,
        matchLengths=[
            [int(matchLength) for matchLength in matchLengthRow]
            for matchLengthRow in matchLengths
        ],
        cooperationRates=cooperationRates,
        payoffMatrix=[[float(value) for value in row] for row in payoffMatrix],
        scoreStatistics=scoreStats,
        playerResults=[
            PlayerResult(
                name=playerNames[i],
                score=playerScores[i],
                rank=rankedNames.index(playerNames[i]) + 1,
                wins=wins[i],
                cooperationRate=cooperationRates[i],
            )
            for i in range(len(players))
        ],
    )

    return iterationResults
