"""
Helper function to generate and save tournament visualizations.
"""

from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from models import TournamentIterationResult


def generateVisualizations(
    allResults: List[TournamentIterationResult],
    outputDir: str,
) -> Dict[str, str]:
    """
    Generates and saves visualizations from tournament results.

    Creates:
    - Score distribution boxplots
    - Win distribution bar charts
    - Cooperation rate heatmaps
    - Average payoff matrix heatmaps
    - Top players comparison charts
    - Score trends across iterations

    Args:
        allResults: List of all tournament iteration results
        outputDir: Directory to save visualizations

    Returns:
        Dictionary with paths to saved visualization files
    """
    outputPath = Path(outputDir)
    outputPath.mkdir(parents=True, exist_ok=True)

    savedFiles = {}
    sns.set_style("whitegrid")

    # Extract data for visualizations
    if not allResults or "playerResults" in allResults[0]:
        print("Generating visualizations...")

        # Aggregate player statistics across iterations
        playerStats = {}
        for iteration in allResults:
            if "error" in iteration:
                continue

            for playerResult in iteration["playerResults"]:
                playerName = playerResult["name"]

                if playerName not in playerStats:
                    playerStats[playerName] = {
                        "scores": [],
                        "ranks": [],
                        "wins": [],
                        "cooperationRates": [],
                    }

                playerStats[playerName]["scores"].append(playerResult["score"])
                playerStats[playerName]["ranks"].append(playerResult["rank"])
                playerStats[playerName]["wins"].append(playerResult["wins"])
                playerStats[playerName]["cooperationRates"].append(
                    playerResult["cooperationRate"]
                )

        # 1. Score Distribution Boxplot (Top 20 players by avg score)
        avgScores = {
            name: sum(stats["scores"]) / len(stats["scores"])
            for name, stats in playerStats.items()
        }
        topPlayers = sorted(avgScores.items(), key=lambda x: x[1], reverse=True)[:20]
        topPlayerNames = [name for name, _ in topPlayers]

        fig, ax = plt.subplots(figsize=(16, 10))
        scoreData = [playerStats[name]["scores"] for name in topPlayerNames]
        ax.boxplot(scoreData, labels=topPlayerNames)
        ax.set_xlabel("Player", fontsize=12)
        ax.set_ylabel("Score", fontsize=12)
        ax.set_title(
            "Score Distribution - Top 20 Players", fontsize=14, fontweight="bold"
        )
        plt.xticks(rotation=90, ha="right")
        plt.tight_layout()
        scorePath = outputPath / "score_distribution_top20.png"
        plt.savefig(scorePath, dpi=300, bbox_inches="tight")
        plt.close()
        savedFiles["scoreDistribution"] = str(scorePath)
        print(f"Saved score distribution to: {scorePath}")

        # 2. Total Wins Bar Chart (Top 20 players)
        totalWins = {name: sum(stats["wins"]) for name, stats in playerStats.items()}
        topWinners = sorted(totalWins.items(), key=lambda x: x[1], reverse=True)[:20]

        fig, ax = plt.subplots(figsize=(14, 8))
        names = [name for name, _ in topWinners]
        wins = [w for _, w in topWinners]
        bars = ax.barh(range(len(names)), wins)
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names)
        ax.set_xlabel("Total Wins", fontsize=12)
        ax.set_title("Total Wins - Top 20 Players", fontsize=14, fontweight="bold")
        ax.invert_yaxis()

        # Color bars by value
        cmap = plt.cm.get_cmap("viridis")
        normalize = plt.Normalize(vmin=min(wins), vmax=max(wins))
        for i, bar in enumerate(bars):
            bar.set_color(cmap(normalize(wins[i])))

        plt.tight_layout()
        winsPath = outputPath / "total_wins_top20.png"
        plt.savefig(winsPath, dpi=300, bbox_inches="tight")
        plt.close()
        savedFiles["totalWins"] = str(winsPath)
        print(f"Saved total wins chart to: {winsPath}")

        # 3. Cooperation Rates Heatmap (Top 30 players)
        topCoopPlayers = sorted(avgScores.items(), key=lambda x: x[1], reverse=True)[
            :30
        ]
        topCoopNames = [name for name, _ in topCoopPlayers]

        coopData = []
        for name in topCoopNames:
            avgCoop = sum(playerStats[name]["cooperationRates"]) / len(
                playerStats[name]["cooperationRates"]
            )
            avgScore = sum(playerStats[name]["scores"]) / len(
                playerStats[name]["scores"]
            )
            coopData.append([avgCoop, avgScore])

        fig, ax = plt.subplots(figsize=(8, 12))
        im = ax.imshow([[row[0]] for row in coopData], cmap="RdYlGn", aspect="auto")
        ax.set_yticks(range(len(topCoopNames)))
        ax.set_yticklabels(topCoopNames, fontsize=8)
        ax.set_xticks([0])
        ax.set_xticklabels(["Cooperation Rate"])
        ax.set_title(
            "Average Cooperation Rate - Top 30 Players", fontsize=14, fontweight="bold"
        )

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label("Cooperation Rate", fontsize=10)

        # Add values as text
        for i, row in enumerate(coopData):
            ax.text(0, i, f"{row[0]:.2%}", ha="center", va="center", fontsize=7)

        plt.tight_layout()
        coopPath = outputPath / "cooperation_rates_top30.png"
        plt.savefig(coopPath, dpi=300, bbox_inches="tight")
        plt.close()
        savedFiles["cooperationRates"] = str(coopPath)
        print(f"Saved cooperation rates to: {coopPath}")

        # 4. Average Rank Comparison (Top 20 players)
        avgRanks = {
            name: sum(stats["ranks"]) / len(stats["ranks"])
            for name, stats in playerStats.items()
        }
        topRankedPlayers = sorted(avgRanks.items(), key=lambda x: x[0])[:20]

        fig, ax = plt.subplots(figsize=(14, 8))
        names = [name for name, _ in topRankedPlayers]
        ranks = [r for _, r in topRankedPlayers]
        bars = ax.barh(range(len(names)), ranks)
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names)
        ax.set_xlabel("Average Rank", fontsize=12)
        ax.set_title(
            "Average Rank - Top 20 Players (Lower is Better)",
            fontsize=14,
            fontweight="bold",
        )
        ax.invert_yaxis()

        # Color bars by value (reverse colormap for ranks)
        cmap = plt.cm.get_cmap("RdYlGn_r")
        normalize = plt.Normalize(vmin=min(ranks), vmax=max(ranks))
        for i, bar in enumerate(bars):
            bar.set_color(cmap(normalize(ranks[i])))

        plt.tight_layout()
        rankPath = outputPath / "average_rank_top20.png"
        plt.savefig(rankPath, dpi=300, bbox_inches="tight")
        plt.close()
        savedFiles["averageRank"] = str(rankPath)
        print(f"Saved average rank chart to: {rankPath}")

        # 5. Score Trends Across Iterations (Top 10 players)
        if len(allResults) > 1:
            topTrendPlayers = sorted(
                avgScores.items(), key=lambda x: x[1], reverse=True
            )[:10]
            topTrendNames = [name for name, _ in topTrendPlayers]

            fig, ax = plt.subplots(figsize=(14, 8))
            for name in topTrendNames:
                scores = playerStats[name]["scores"]
                iterations = list(range(1, len(scores) + 1))
                ax.plot(iterations, scores, marker="o", label=name, linewidth=2)

            ax.set_xlabel("Iteration", fontsize=12)
            ax.set_ylabel("Score", fontsize=12)
            ax.set_title(
                "Score Trends Across Iterations - Top 10 Players",
                fontsize=14,
                fontweight="bold",
            )
            ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=9)
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            trendPath = outputPath / "score_trends_top10.png"
            plt.savefig(trendPath, dpi=300, bbox_inches="tight")
            plt.close()
            savedFiles["scoreTrends"] = str(trendPath)
            print(f"Saved score trends to: {trendPath}")

        # 6. Payoff Matrix Heatmap (if available)
        if "payoffMatrix" in allResults[0]:
            # Average payoff matrix across all iterations
            payoffMatrices = [
                np.array(iteration["payoffMatrix"])
                for iteration in allResults
                if "payoffMatrix" in iteration and "error" not in iteration
            ]

            if payoffMatrices:
                avgPayoffMatrix = np.mean(payoffMatrices, axis=0)
                playerNames = allResults[0]["playerNames"]

                # Only visualize top 30 players for readability
                topPayoffPlayers = sorted(
                    avgScores.items(), key=lambda x: x[1], reverse=True
                )[:30]
                topPayoffNames = [name for name, _ in topPayoffPlayers]
                topIndices = [playerNames.index(name) for name in topPayoffNames]

                subMatrix = avgPayoffMatrix[np.ix_(topIndices, topIndices)]

                fig, ax = plt.subplots(figsize=(16, 14))
                im = ax.imshow(subMatrix, cmap="YlOrRd", aspect="auto")
                ax.set_xticks(range(len(topPayoffNames)))
                ax.set_yticks(range(len(topPayoffNames)))
                ax.set_xticklabels(topPayoffNames, rotation=90, ha="right", fontsize=7)
                ax.set_yticklabels(topPayoffNames, fontsize=7)
                ax.set_title(
                    "Average Payoff Matrix - Top 30 Players",
                    fontsize=14,
                    fontweight="bold",
                )

                # Add colorbar
                cbar = plt.colorbar(im, ax=ax)
                cbar.set_label("Average Score", fontsize=10)

                plt.tight_layout()
                payoffPath = outputPath / "payoff_matrix_top30.png"
                plt.savefig(payoffPath, dpi=300, bbox_inches="tight")
                plt.close()
                savedFiles["payoffMatrix"] = str(payoffPath)
                print(f"Saved payoff matrix to: {payoffPath}")

        print(f"\nAll visualizations saved to: {outputPath}")
        return savedFiles

    else:
        print("No valid results to visualize")
        return {}
