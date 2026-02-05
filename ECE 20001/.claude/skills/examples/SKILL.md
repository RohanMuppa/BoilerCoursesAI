---
user_invocable: true
description: Find worked examples in the ECE 20001 textbook
---

# Find Examples

Find worked examples in the ECE 20001 textbook related to a topic.

## Workflow

1. First check the ECE 20001 context_db/examples folder for saved examples
2. Use the local-rag MCP query_documents tool to search the ingested textbook for example problems
3. Return the examples with full worked solutions and approximate page numbers
4. Calculate page number from chunkIndex by dividing by 7

## Usage

$ARGUMENTS contains the topic to find examples for.
