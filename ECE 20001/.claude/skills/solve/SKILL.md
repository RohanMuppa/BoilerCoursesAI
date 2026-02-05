---
user_invocable: true
description: Solve ECE 20001 problems with verification workflow
---

# Solve Problem

Solve an ECE 20001 problem using the hybrid workflow. Show solver work immediately, then append verification results.

## Workflow (Hybrid Approach)

1. Launch Solver Agent in foreground to work through the problem step by step
2. IMMEDIATELY show the solver's work and preliminary answer to the user
3. Launch Arithmetic Checker Agent and Textbook Method Agent in BACKGROUND (parallel)
4. While verification runs, tell the user "Verification in progress..."
5. When verification completes, append results
6. If errors found, clearly mark corrections and show the corrected answer

## Why Hybrid

This approach lets the user follow along with the solution process while verification happens in parallel. If verification passes, the preliminary answer is confirmed. If errors are found, corrections are clearly shown.

## Solver Agent

Work through the problem step by step, showing all work and arriving at a solution. This runs in foreground so the user sees progress.

## Arithmetic Checker Agent (Background)

Independently verify all arithmetic, calculations, and numerical steps. Catch computational errors, sign mistakes, and algebraic manipulation errors. Run with run_in_background: true.

## Textbook Method Agent (Background)

First check the ECE 20001 context_db for relevant formulas and methods. Then use the local-rag MCP query_documents tool to search the ingested textbook for similar problems and their solutions. Use these as a guide for how the current problem should be solved. Also find relevant sections, examples, and methods. Verify the solution uses EXACTLY the same methods, notation, and approach taught in the book. Flag any deviations from the textbook methodology, even if mathematically valid. Run with run_in_background: true.

## Output Format

Present solver results first with a note that verification is running. Then append verification results when ready. Format final answer clearly at the end.

## Usage

$ARGUMENTS contains the problem statement or image to solve.
