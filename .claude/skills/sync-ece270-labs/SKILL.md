---
name: sync-ece270-labs
description: Sync new ECE 270 labs from GitHub without overwriting existing work
allowed-tools: Bash
argument-hint: (no arguments needed)
---

# Sync ECE 270 Labs

Run the sync script to pull new labs from the ECE 270 GitHub repository.

CRITICAL: NEVER use git pull directly on the student-labs-main folder. This will overwrite the user's completed work.

ALWAYS use the sync script which only adds NEW labs that don't exist locally. Existing lab folders and files are never touched.

## Instructions

The workspace path is stored in config.json. Run the sync script using this command:

```bash
WORKSPACE=$(python3 -c "import json; print(json.load(open('config.json'))['workspace_path'])") && cd "$WORKSPACE" && python3 scripts/sync_ece270_labs.py
```

Report the results to the user, showing which new labs were added (if any) or confirming they are already up to date.
