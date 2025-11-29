# AXL-Bench: LLM Performance in Axelrod Tournament Strategies

## Overview

AXL-Bench is a benchmark designed to evaluate Large Language Models (LLMs) in game theory settings by testing their performance against classic strategies from the Axelrod tournaments. This benchmark assesses how well LLMs can adapt, learn, and compete in iterated prisoner's dilemma scenarios against well-known strategies that have been extensively studied in game theory literature.

A central research question underlying this benchmark is whether token prediction during pre-training implies that LLMs have learned strategic game theory concepts from textual format. Since LLMs are trained on vast corpora that likely contain discussions of game theory, the prisoner's dilemma, and strategic decision-making, this benchmark investigates whether such textual knowledge translates into actual strategic competence when LLMs must make decisions in interactive game settings.

## Background: Axelrod Tournaments

The Axelrod tournaments, conducted by political scientist Robert Axelrod in the 1980s, were a series of computer tournaments where different strategies for playing the iterated prisoner's dilemma competed against each other. These tournaments revealed fundamental insights about cooperation, reciprocity, and strategic behavior.

The most famous result was the success of **Tit-for-Tat**, a simple strategy that:

- Cooperates on the first move
- Then mirrors the opponent's previous move

This strategy won both tournaments, demonstrating that cooperation can emerge and be stable even in competitive environments.

## Benchmark Design

### Game Theory Setting

The benchmark uses the **Iterated Prisoner's Dilemma** as the core game:

- **Players**: An LLM agent vs. a classic Axelrod tournament strategy
- **Actions**: Cooperate (C) or Defect (D)
- **Payoff Matrix**:
  - Mutual Cooperation: (R, R) - Reward for both
  - Mutual Defection: (P, P) - Punishment for both
  - Temptation to Defect: (T, S) - Temptation vs. Sucker's payoff
  - Sucker's Payoff: (S, T) - Sucker's payoff vs. Temptation

Standard values: T=5, R=3, P=1, S=0

### Evaluation Metrics

The benchmark measures LLM performance using:

1. **Total Score**: Cumulative payoff across all rounds
2. **Win Rate**: Percentage of games won against each strategy
3. **Cooperation Rate**: Percentage of cooperative moves
4. **Adaptability**: Ability to adjust strategy based on opponent behavior
5. **Efficiency**: Score relative to optimal strategy for each opponent

## Research Questions

This benchmark addresses several important questions:

1. Does token prediction imply strategic learning? Can LLMs that learned about game theory through textual training data actually apply these concepts in interactive decision-making scenarios?
2. Can LLMs learn to cooperate in iterated games?
3. Do LLMs recognize and adapt to different opponent strategies?
4. How do LLMs compare to classic game theory strategies?
5. Can LLMs discover optimal strategies like Tit-for-Tat?
6. Do LLMs exhibit consistent strategic behavior or random responses?
7. Textual knowledge vs. strategic competence: Is there a gap between what LLMs know about game theory (from text) and their ability to execute strategic decisions in practice?
