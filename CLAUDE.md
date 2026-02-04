# Claude Rules

## Automatic Actions
EVERY TIME a new chat session begins, immediately ask the user if they want to pull the latest files from Google Drive. Run the pull_ece_files.py script if they say yes. This script syncs ALL configured course folders from Google Drive, not just ECE files. This prompt must appear at the start of every conversation before addressing any other requests.

## Course Folders
ECE 270 is stored locally only, not on Google Drive. Do not offer to pull ECE 270 files from Google Drive.
ECE 39595EE is synced from Google Drive.

## Context Database

Each course has a local context_db folder containing class specific context that should be searched BEFORE looking through textbooks. This provides faster, more relevant answers for common questions.

### Search Priority
1. First search the course context_db folder for matching entries
2. Only search the textbook if context_db does not have relevant information
3. Use textbook references in context_db entries to guide deeper searches when needed

### Context Database Structure
Each course folder contains a context_db subfolder with JSON files organized by category. The .schema.json file in each context_db defines the available categories and entry format for that course.

Common categories include formulas, concepts, examples, lecture_notes, and course specific categories like lab_notes for ECE 270 or verilog patterns.

### Adding Context
When you learn something new or solve a problem, consider adding it to the appropriate context_db category. Each entry should have an id, title, content, keywords for searching, and optionally related_textbook_sections for cross referencing.

### Available Context Databases
ECE 20001 context_db for circuits and electrical fundamentals
ECE 270 context_db for digital design and SystemVerilog
ECE 39595EE context_db for engineering innovation course
HONR 299 context_db for honors seminar materials

## Formatting
NEVER use arrows (→, ←, ↓, ↑)
NEVER use em dashes (—) or en dashes (–)
NEVER use hyphens (-)
NEVER use colons (:)
NEVER use bullet points (-, *, •)
NEVER use emojis
NEVER use excessive line breaks
NEVER use tables
Use commas and periods instead

---

# Google Drive API Project

Python implementation for reading and updating files from Google Drive.

## Files

All Python files are in the scripts folder.

google_drive_api.py is the OAuth 2.0 client for user based auth.
google_drive_service_account.py is the Service Account client for server to server auth.
pull_ece_files.py pulls files from all configured Google Drive folders to local storage.
requirements.txt contains Python dependencies.

## OAuth 2.0 vs Service Account

### OAuth 2.0 (`google_drive_api.py`)
**Use when:** Building apps that access user data with their consent

| Pros | Cons |
|------|------|
| Access user's personal Drive | Requires user interaction (browser) |
| No file sharing needed | Token expires, needs refresh |
| Standard for user-facing apps | More complex auth flow |

**Setup:**
1. Create OAuth 2.0 credentials (Desktop app) in Google Cloud Console
2. Download as `credentials.json`
3. First run opens browser for consent

### Service Account (`google_drive_service_account.py`)
**Use when:** Server-to-server automation, no user interaction

| Pros | Cons |
|------|------|
| No user interaction needed | Files must be shared with service account |
| Runs headless on servers | Has its own Drive (empty by default) |
| No token expiration handling | Can't access user files without sharing |

**Setup:**
1. Create Service Account in IAM & Admin
2. Download JSON key as `service_account.json`
3. Share Drive files/folders with service account email

## Quick Start

```bash
# Create virtual environment (first time only)
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run (after adding credentials.json)
python3 scripts/google_drive_api.py
```

## Re-entering the Virtual Environment

After closing your terminal, re-activate with:

```bash
cd /path/to/workspace
source venv/bin/activate
```

To deactivate when done:
```bash
deactivate
```

## API Methods

```python
# Initialize and authenticate
drive = GoogleDriveAPI()  # or GoogleDriveServiceAccount()
drive.authenticate()

# List files
files = drive.list_files(page_size=10)
files = drive.list_files(folder_id="FOLDER_ID")
files = drive.search_files("report")

# Read files
content = drive.read_file(file_id)           # Returns bytes
text = drive.read_file_as_text(file_id)      # Returns string
exported = drive.export_google_doc(file_id)  # Export Google Docs

# Write/Update files
drive.update_file(file_id, "new content")
drive.create_file("new.txt", "content")
drive.upload_file("/local/path/file.pdf")
drive.delete_file(file_id)
```

## Getting File IDs

File ID is in the URL when viewing in Google Drive:
```
https://drive.google.com/file/d/FILE_ID_HERE/view
https://docs.google.com/document/d/DOC_ID_HERE/edit
```

## Export Formats for Google Docs

| Source | mime_type |
|--------|-----------|
| Docs | `text/plain`, `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Sheets | `text/csv`, `application/pdf`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| Slides | `application/pdf`, `application/vnd.openxmlformats-officedocument.presentationml.presentation` |

## Using Environment Variables (Recommended)

Instead of storing tokens in files, use environment variables:

| Variable | Contains |
|----------|----------|
| `GOOGLE_DRIVE_TOKEN` | OAuth token JSON |
| `GOOGLE_DRIVE_CREDENTIALS` | OAuth client credentials JSON |

**Setup:**

1. Run the script once with `credentials.json` to authenticate
2. After auth, the token JSON is printed to the console
3. Copy the token and set it as an env var:

```bash
# Add to ~/.zshrc or ~/.bashrc
export GOOGLE_DRIVE_TOKEN='{"token": "...", "refresh_token": "...", ...}'

# Optional: also store credentials
export GOOGLE_DRIVE_CREDENTIALS='{"installed": {"client_id": "...", ...}}'
```

4. Reload your shell: `source ~/.zshrc`
5. Delete the local files:

```bash
rm token.json credentials.json
```

**Priority order:**
1. Environment variable (if `use_env_vars=True`, the default)
2. Local file

## Domain-Wide Delegation (Service Account)

To access any user's files in a Google Workspace domain:

1. Enable domain-wide delegation for service account
2. Admin adds scopes in Google Admin Console
3. Use `delegated_user` parameter:

```python
drive = GoogleDriveServiceAccount(delegated_user="user@company.com")
```
