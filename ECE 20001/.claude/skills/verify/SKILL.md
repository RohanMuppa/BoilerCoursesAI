---
user_invocable: true
description: Verify existing solutions against textbook methods
---

# Verify Solution

Verify existing work against textbook methods without resolving the problem.

## Workflow

1. Launch Arithmetic Checker Agent to verify calculations
2. Launch Textbook Method Agent to verify methods match the textbook
3. Report any errors or deviations found

## Arithmetic Checker Agent

Independently verify all arithmetic, calculations, and numerical steps. Catch computational errors, sign mistakes, and algebraic manipulation errors.

## Textbook Method Agent

First check the ECE 20001 context_db for relevant formulas and methods. Then use the local-rag MCP query_documents tool to search the ingested textbook for similar problems and their solutions. Compare the submitted solution against how the textbook solves similar problems. Verify the solution uses EXACTLY the same methods, notation, and approach taught in the book. Flag any deviations.

## Usage

$ARGUMENTS contains the solution to verify.
