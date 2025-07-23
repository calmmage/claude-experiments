# Claude Experiments Project

## Overview

This project automates daily runs of Claude Code to generate cool programming experiments. With a Claude Max subscription, we'll have an automated system that creates innovative code experiments every day.

## Project Structure

### Component 1: Runner
A standalone script that executes Claude Code to generate experiments.
- One-off execution (triggered by external scheduler)
- Manages Claude Code interactions
- Stores results in organized structure

### Component 2: Experiments
A folder containing all generated experiments with organized naming:
- Format: `day_X_experiment_name` or `YYYY-MM-DD_experiment_name`
- Each experiment in its own directory
- Preserves full experiment history

## Tech Stack

### Python
- **Package Manager**: uv (modern, fast Python package manager)
- **Key libraries**: As needed per experiment

### Other Languages
- Use language-appropriate tools and package managers
- Node.js: npm/yarn/pnpm
- Rust: cargo
- Go: go modules
- etc.

## Execution Flow

1. External scheduler triggers the runner script
2. Claude Code generates a new experiment idea
3. Implements the experiment with full code
4. Saves to experiments folder with proper naming
5. Logs the run and any interesting outcomes

## Goals

- Build a collection of innovative code experiments
- Explore Claude's creative coding capabilities
- Create potentially useful tools, libraries, or demos
- Learn from AI-generated patterns and solutions