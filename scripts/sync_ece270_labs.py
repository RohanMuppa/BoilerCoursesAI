#!/usr/bin/env python3
"""
Sync new ECE 270 labs without touching existing content.
Run: python3 sync_ece270_labs.py
"""
import subprocess
import tempfile
import shutil
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR.parent / "config.json"
COURSE_REPO = "https://github.com/ece270/student-labs.git"


def load_config():
    """Load configuration from config.json"""
    if not CONFIG_PATH.exists():
        print("Error: config.json not found.")
        print("Copy config.example.json to config.json and fill in your values.")
        sys.exit(1)

    with open(CONFIG_PATH) as f:
        return json.load(f)


def get_lab_folders(path):
    """Get all labX folders in a directory."""
    return {
        d.name for d in Path(path).iterdir()
        if d.is_dir() and d.name.startswith("lab") and d.name[3:].isdigit()
    }


def sync():
    config = load_config()
    base_path = Path(config["workspace_path"])

    # Get ECE 270 config
    ece270_config = config["courses"].get("ECE 270", {})
    local_folder = ece270_config.get("local_folder_name", "ECE 270")
    labs_path = ece270_config.get("labs_path", "student-labs-main")

    local_path = base_path / local_folder / labs_path

    print("Checking for new ECE 270 labs...")

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_path = Path(tmpdir) / "student-labs"

        result = subprocess.run(
            ["git", "clone", "--depth", "1", COURSE_REPO, str(clone_path)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Failed to clone repo: {result.stderr}")
            return

        remote_labs = get_lab_folders(clone_path)
        local_labs = get_lab_folders(local_path)
        new_labs = remote_labs - local_labs

        if not new_labs:
            print("No new labs available. You're up to date.")
            return

        print(f"Found {len(new_labs)} new lab(s)!")

        for lab in sorted(new_labs):
            src = clone_path / lab
            dst = local_path / lab
            shutil.copytree(src, dst)
            print(f"  Added: {lab}")

        # Sync new files in refs/ without overwriting existing
        remote_refs = clone_path / "refs"
        local_refs = local_path / "refs"
        new_refs = []

        if remote_refs.exists():
            for item in remote_refs.rglob("*"):
                if item.is_file():
                    relative = item.relative_to(remote_refs)
                    target = local_refs / relative
                    if not target.exists():
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, target)
                        new_refs.append(str(relative))

        if new_refs:
            print(f"  Added {len(new_refs)} new reference file(s)")

    print("Sync complete.")

if __name__ == "__main__":
    sync()
