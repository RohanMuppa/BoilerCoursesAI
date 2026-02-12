# BoilerCourses-AI

Your AI powered academic command center.

Stop digging through 900 page textbooks. Stop hunting for that one lecture slide from week 3. Stop manually downloading files from 6 different Google Drive folders. Stop switching between Brightspace, Google Drive, and your notes app.

BoilerCourses-AI combines local semantic search, intelligent file organization, and direct Brightspace access into one unified workspace. Ask questions in plain English and get answers pulled directly from your course materials. Check your assignments and grades without opening a browser.

The real power is generative interactive content. Tell Claude any topic you need to learn and it generates comprehensive HTML tutorials with visualizations, animations, tabbed navigation, and practice problems. Organic chemistry mechanisms with electron flow animations. Economics supply and demand curves you can drag. Physics free body diagrams that respond to changing forces. Any subject, any concept. These are standalone files you open in any browser, thorough enough to learn entire topics without the lecture.

Powered by Claude Code CLI, local RAG, and the Brightspace MCP.

<p align="center">
  <img src="assets/architecture-overview.svg" alt="System Architecture" width="800"/>
</p>

## Features

### Interactive Study Guides (Flagship Feature)

<p align="center">
  <img src="assets/interactive-content.svg" alt="Interactive Content Generation" width="800"/>
</p>

Tell Claude any topic and it generates a complete, standalone HTML tutorial you can open in any browser. Each tutorial includes deep explanations covering the why and how, numerous worked examples with step by step solutions, intuitive analogies that make abstract concepts concrete, common student mistakes highlighted, 10 to 15 practice problems with detailed solutions, and interactive visualizations from draggable graphs to animated diagrams. The included CLAUDE.md files contain optimized instructions for generating these consistently.

### Textbook Search (Local RAG)

<p align="center">
  <img src="assets/rag-pipeline.svg" alt="RAG Pipeline" width="800"/>
</p>

Ingest a 900 page PDF and search it by meaning, not keywords. Ask "how do flip flops work" and find the exact pages that explain sequential circuits, even if those pages never use the phrase "flip flop." Each course also has a local context_db that stores class specific knowledge and is searched before the textbook for faster answers.

```
ingest_file("/path/to/textbook.pdf")
query_documents("karnaugh map simplification", limit=5)
```

Results include a chunk index (divide by 7 for approximate page number) and a relevance score from 0 (perfect) to 1 (weak).

### Google Drive Sync

One command pulls lecture slides, assignments, and notes from all your configured Google Drive folders.

```bash
python3 scripts/pull_ece_files.py
```

Supports both OAuth 2.0 for personal accounts and Service Account for shared course folders.

### Brightspace Integration

Query your courses, assignments, and grades through Claude using natural language. "What assignments are due this week?" or "Show my grades for ECE 270." Source available at github.com/RohanMuppa/brightspace-mcp-server

### Multi-Agent Verification

<p align="center">
  <img src="assets/verification-workflow.svg" alt="Verification Workflow" width="800"/>
</p>

For technical problems like circuit analysis, a multi-agent workflow parses the problem, looks up textbook methods, solves symbolically with SymPy, then runs three independent checkers in parallel for units, physical sanity, and methodology compliance. Reports a confidence level so you know how much to trust the answer.

## Quick Start

```bash
git clone https://github.com/RohanMuppa/boilercourses-ai.git
cd boilercourses-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Install Claude Code CLI from claude.ai/claude-code, then run `claude` in the project directory. Claude automatically reads CLAUDE.md and understands your project structure.

For Google Drive sync, create OAuth 2.0 credentials in Google Cloud Console and download as credentials.json. For PDF image extraction, install poppler (`brew install poppler` on macOS, `sudo apt-get install poppler-utils` on Ubuntu).

## Project Structure

```
boilercourses-ai/
    ECE-20001/                       # Course folder (any course works)
        lectures/
        labs/
        homework/
        exams/
        explanations/                # Generated interactive HTML tutorials
        context_db/                  # Class specific knowledge (JSON)
        CLAUDE.md                    # Course specific instructions
    textbooks/                       # PDF textbooks (gitignored)
    scripts/
        google_drive_api.py          # OAuth 2.0 client
        google_drive_service_account.py
        pull_ece_files.py            # Sync all configured courses
        requirements.txt
    lancedb/                         # Vector database (gitignored)
    .mcp.json                        # MCP server configuration (gitignored)
    CLAUDE.md                        # Global instructions
    README.md
```

Each course folder follows this pattern. Add as many as you need.

## Adding a New Course

Create the folder structure, add the course to config.json, create a context_db/.schema.json defining categories for that subject, ingest your textbook with `ingest_file()`, and create a CLAUDE.md with course specific rules. Copy an existing course folder as a starting point.

## Requirements

Python 3.8+, Claude Code CLI, Node.js (for MCP servers). Optional. Google Cloud project with Drive API enabled, poppler for PDF image extraction.

## License

MIT License. Free for personal and educational use.
