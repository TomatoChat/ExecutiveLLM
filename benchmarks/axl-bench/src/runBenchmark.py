#!/usr/bin/env python3
"""
Main benchmark script for running comprehensive Axelrod tournament with LLM players.

This script runs tournaments with:
- All standard Axelrod strategies
- All LLM models (Claude, OpenAI, Gemini) with different prompts
- Grounding-enabled LLM models

Results are saved with comprehensive metrics and visualizations.
"""

import argparse
import time
from datetime import datetime
from typing import List

import axelrod as axl
from dotenv import load_dotenv

from .helpers.generateLlmPlayers import generateLlmPlayers
from .helpers.generateVisualizations import generateVisualizations
from .helpers.runTournamentIteration import runTournamentIteration
from .helpers.saveResults import saveResults
from .models import BenchmarkMetadata, TournamentIterationResult

load_dotenv()


def main():
    """Main function to run the benchmark."""
    parser = argparse.ArgumentParser(
        description="Run comprehensive Axelrod tournament benchmark with LLM players"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        required=True,
        help="Number of times to run the tournament",
    )
    parser.add_argument(
        "--turns",
        type=int,
        required=True,
        help="Number of turns per match in the tournament",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="benchmark_results",
        help="Output directory for results (default: benchmark_results)",
    )
    parser.add_argument(
        "--skip-regular",
        action="store_true",
        help="Skip regular (non-grounding) LLM models",
    )
    parser.add_argument(
        "--skip-grounding",
        action="store_true",
        help="Skip grounding-enabled LLM models",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=1024,
        help="Maximum tokens for LLM responses (default: 1024)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Temperature parameter for LLMs (default: 1.0)",
    )

    args = parser.parse_args()

    if args.skip_regular and args.skip_grounding:
        print("ERROR: Cannot skip both regular and grounding models!")
        return

    print("=" * 80)
    print("AXELROD TOURNAMENT BENCHMARK WITH LLM PLAYERS")
    print("=" * 80)
    print("\nConfiguration:")
    print(f"  Iterations: {args.iterations}")
    print(f"  Turns per match: {args.turns}")
    print(f"  Random seed: {args.seed}")
    print(f"  Output directory: {args.output_dir}")
    print(f"  Include regular models: {not args.skip_regular}")
    print(f"  Include grounding models: {not args.skip_grounding}")
    print(f"  Max tokens: {args.max_tokens}")
    print(f"  Temperature: {args.temperature}")

    benchmarkStartTime = time.time()

    # Step 1: Get all Axelrod strategies
    print("\n" + "=" * 80)
    print("STEP 1: Loading Axelrod Strategies")
    print("=" * 80)

    axelrodStrategies: List[axl.Player] = [strategy() for strategy in axl.strategies]

    print(f"Loaded {len(axelrodStrategies)} Axelrod strategies")

    # Step 2: Generate all LLM players
    print("\n" + "=" * 80)
    print("STEP 2: Generating LLM Players")
    print("=" * 80)

    llmPlayers: List[axl.Player] = generateLlmPlayers(
        numTurns=args.turns,
        includeRegular=not args.skip_regular,
        includeGrounding=not args.skip_grounding,
        maxTokens=args.max_tokens,
        temperature=args.temperature,
    )

    print(f"Generated {len(llmPlayers)} LLM players")

    # Step 3: Combine all players
    allPlayers: List[axl.Player] = axelrodStrategies + llmPlayers
    print(f"\nTotal players: {len(allPlayers)}")
    print(f"  - Axelrod strategies: {len(axelrodStrategies)}")
    print(f"  - LLM players: {len(llmPlayers)}")

    # Step 4: Run tournament iterations
    print("\n" + "=" * 80)
    print("STEP 3: Running Tournament Iterations")
    print("=" * 80)

    allResults: List[TournamentIterationResult] = []

    for i in range(args.iterations):
        iterationSeed = args.seed + i
        result = runTournamentIteration(
            players=allPlayers,
            turns=args.turns,
            seed=iterationSeed,
            iterationNumber=i + 1,
        )

        allResults.append(result)

    # Step 5: Save results
    print("\n" + "=" * 80)
    print("STEP 4: Saving Results")
    print("=" * 80)

    benchmarkMetadata = BenchmarkMetadata(
        benchmarkDate=datetime.now().isoformat(),
        iterations=args.iterations,
        turnsPerMatch=args.turns,
        baseSeed=args.seed,
        totalPlayers=len(allPlayers),
        numAxelrodStrategies=len(axelrodStrategies),
        numLlmPlayers=len(llmPlayers),
        includeRegularModels=not args.skip_regular,
        includeGroundingModels=not args.skip_grounding,
        maxTokens=args.max_tokens,
        temperature=args.temperature,
    )

    savedFiles = saveResults(
        allResults=allResults,
        benchmarkMetadata=benchmarkMetadata,
        outputDir=args.output_dir,
    )

    # Step 6: Generate visualizations
    print("\n" + "=" * 80)
    print("STEP 5: Generating Visualizations")
    print("=" * 80)

    # Get the output directory for this run (last part of the full results path)
    runOutputDir = savedFiles["fullResults"].rsplit("/", 1)[0]

    visualizationFiles = generateVisualizations(
        allResults=allResults,
        outputDir=runOutputDir,
    )

    savedFiles.update(visualizationFiles)

    # Step 7: Print summary
    benchmarkEndTime = time.time()
    totalDuration = benchmarkEndTime - benchmarkStartTime

    print("\n" + "=" * 80)
    print("BENCHMARK COMPLETE")
    print("=" * 80)
    print(f"\nTotal duration: {totalDuration / 60:.2f} minutes")
    print(f"Average time per iteration: {totalDuration / args.iterations:.2f} seconds")

    print("\n" + "-" * 80)
    print("Saved Files:")
    print("-" * 80)
    for fileType, filePath in savedFiles.items():
        print(f"  {fileType}: {filePath}")

    print("\n" + "=" * 80)
    print("Results saved to:", runOutputDir)
    print("=" * 80)


if __name__ == "__main__":
    main()
