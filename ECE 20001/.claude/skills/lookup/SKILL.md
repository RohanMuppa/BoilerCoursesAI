---
user_invocable: true
description: Query the ECE 20001 textbook for topics and formulas
---

# Lookup Textbook

Query the ECE 20001 textbook for a specific topic, formula, or method.

## Workflow

1. First check the ECE 20001 context_db folder for relevant entries
2. Use the local-rag MCP query_documents tool to search the ingested textbook
3. Return the relevant content with chunk references and approximate page numbers
4. If context_db has related_textbook_sections, use those to guide the search

## Usage

$ARGUMENTS contains the topic, concept, or formula to look up.
