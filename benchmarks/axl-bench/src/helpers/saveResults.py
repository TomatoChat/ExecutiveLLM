"""
Helper function to save tournament results to files.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd

from ..models import BenchmarkMetadata, TournamentIterationResult


def saveResults(
    allResults: List[TournamentIterationResult],
    benchmarkMetadata: BenchmarkMetadata,
    outputDir: str = "benchmarkResults",
) -> Dict[str, str]:
    """
    Saves tournament results to JSON and CSV files with historical tracking.

    Creates timestamped output directory and saves:
    - Full results as JSON
    - Summary statistics as CSV
    - Per-player results as CSV
    - Benchmark metadata

    Args:
        allResults: List of all tournament iteration results
        benchmarkMetadata: Metadata about the benchmark configuration
        outputDir: Base directory for saving results

    Returns:
        Dictionary with paths to saved files
    """
    # Create timestamped directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    runDir = Path(outputDir) / timestamp
    runDir.mkdir(parents=True, exist_ok=True)

    savedFiles = {}

    # Save full results as JSON
    fullResultsPath = runDir / "full_results.json"
    with open(fullResultsPath, "w") as f:
        json.dump(
            {
                "metadata": benchmarkMetadata.model_dump(),
                "iterations": [result.model_dump() for result in allResults],
            },
            f,
            indent=2,
        )
    savedFiles["fullResults"] = str(fullResultsPath)
    print(f"Saved full results to: {fullResultsPath}")

    # Save metadata separately
    metadataPath = runDir / "metadata.json"
    with open(metadataPath, "w") as f:
        json.dump(benchmarkMetadata.model_dump(), f, indent=2)
    savedFiles["metadata"] = str(metadataPath)
    print(f"Saved metadata to: {metadataPath}")

    # Aggregate results across all iterations
    if allResults and allResults[0].playerResults:
        # Per-player aggregated results
        playerStats = {}

        for iteration in allResults:
            if iteration.error:
                continue

            for playerResult in iteration.playerResults:
                playerName = playerResult.name

                if playerName not in playerStats:
                    playerStats[playerName] = {
                        "scores": [],
                        "ranks": [],
                        "wins": [],
                        "cooperationRates": [],
                    }

                playerStats[playerName]["scores"].append(playerResult.score)
                playerStats[playerName]["ranks"].append(playerResult.rank)
                playerStats[playerName]["wins"].append(playerResult.wins)
                playerStats[playerName]["cooperationRates"].append(
                    playerResult.cooperationRate
                )

        # Calculate summary statistics for each player
        summaryData = []
        for playerName, stats in playerStats.items():
            summaryData.append(
                {
                    "player": playerName,
                    "avgScore": sum(stats["scores"]) / len(stats["scores"]),
                    "minScore": min(stats["scores"]),
                    "maxScore": max(stats["scores"]),
                    "avgRank": sum(stats["ranks"]) / len(stats["ranks"]),
                    "bestRank": min(stats["ranks"]),
                    "worstRank": max(stats["ranks"]),
                    "totalWins": sum(stats["wins"]),
                    "avgWins": sum(stats["wins"]) / len(stats["wins"]),
                    "avgCooperationRate": sum(stats["cooperationRates"])
                    / len(stats["cooperationRates"]),
                    "numIterations": len(stats["scores"]),
                }
            )

        # Sort by average score (descending)
        summaryData.sort(key=lambda x: x["avgScore"], reverse=True)

        # Save summary as CSV
        summaryDf = pd.DataFrame(summaryData)
        summaryCsvPath = runDir / "summaryStatistics.csv"

        summaryDf.to_csv(summaryCsvPath, index=False)

        savedFiles["summary"] = str(summaryCsvPath)
        print(f"Saved summary statistics to: {summaryCsvPath}")

        # Save detailed per-iteration results as CSV
        detailedData = []
        for iteration in allResults:
            if iteration.error:
                continue

            for playerResult in iteration.playerResults:
                detailedData.append(
                    {
                        "iteration": iteration.iteration,
                        "player": playerResult.name,
                        "score": playerResult.score,
                        "rank": playerResult.rank,
                        "wins": playerResult.wins,
                        "cooperationRate": playerResult.cooperationRate,
                    }
                )

        detailedDf = pd.DataFrame(detailedData)
        detailedCsvPath = runDir / "detailedResults.csv"
        detailedDf.to_csv(detailedCsvPath, index=False)
        savedFiles["detailed"] = str(detailedCsvPath)
        print(f"Saved detailed results to: {detailedCsvPath}")

    # Update historical index
    historyPath = Path(outputDir) / "history.json"
    history = []

    if historyPath.exists():
        with open(historyPath, "r") as f:
            history = json.load(f)

    history.append(
        {
            "timestamp": timestamp,
            "directory": str(runDir),
            "metadata": benchmarkMetadata.model_dump(),
            "numIterations": len(allResults),
        }
    )

    with open(historyPath, "w") as f:
        json.dump(history, f, indent=2)
    savedFiles["history"] = str(historyPath)
    print(f"Updated history index: {historyPath}")

    return savedFiles
