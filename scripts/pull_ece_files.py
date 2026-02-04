"""
Pull files from Google Drive folders to local folders.
Syncs all configured course folders.
"""

import os
import json
import sys
from pathlib import Path
from google_drive_api import GoogleDriveAPI

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR.parent / "config.json"


def load_config():
    """Load configuration from config.json"""
    if not CONFIG_PATH.exists():
        print("Error: config.json not found.")
        print("Copy config.example.json to config.json and fill in your values.")
        sys.exit(1)

    with open(CONFIG_PATH) as f:
        return json.load(f)


def sync_folder(drive, drive_folder_name, local_folder_path):
    """Sync a single Google Drive folder to local folder."""
    print(f"\nSearching for folder '{drive_folder_name}' on Google Drive...")

    query = f"name = '{drive_folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
    folders = drive.list_files(query=query, page_size=10)

    if not folders:
        print(f"Folder '{drive_folder_name}' not found on Google Drive.")
        return False

    folder_id = folders[0]['id']
    print(f"Found folder with ID: {folder_id}")

    print(f"Listing files in '{drive_folder_name}'...")
    files = drive.list_files(folder_id=folder_id, page_size=100)

    if not files:
        print("No files found in the folder.")
        return True

    print(f"Found {len(files)} files.")

    os.makedirs(local_folder_path, exist_ok=True)

    for file_info in files:
        file_name = file_info['name']
        file_id = file_info['id']
        mime_type = file_info['mimeType']

        print(f"  Downloading: {file_name}")

        local_path = os.path.join(local_folder_path, file_name)

        try:
            if mime_type == 'application/vnd.google-apps.document':
                content = drive.export_google_doc(file_id, 'application/pdf')
                local_path = local_path + '.pdf' if not local_path.endswith('.pdf') else local_path
            elif mime_type == 'application/vnd.google-apps.spreadsheet':
                content = drive.export_google_doc(file_id, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                local_path = local_path + '.xlsx' if not local_path.endswith('.xlsx') else local_path
            elif mime_type == 'application/vnd.google-apps.presentation':
                content = drive.export_google_doc(file_id, 'application/pdf')
                local_path = local_path + '.pdf' if not local_path.endswith('.pdf') else local_path
            elif mime_type == 'application/vnd.google-apps.folder':
                print(f"    Skipping subfolder: {file_name}")
                continue
            else:
                content = drive.read_file(file_id)

            with open(local_path, 'wb') as f:
                f.write(content)
            print(f"    Saved to: {local_path}")

        except Exception as e:
            print(f"    Error downloading {file_name}: {e}")

    return True


def list_available_folders(drive):
    """List all available folders on Google Drive."""
    print("\nAvailable folders on Google Drive:")
    all_folders = drive.list_files(
        query="mimeType = 'application/vnd.google-apps.folder'",
        page_size=50
    )
    for f in all_folders:
        print(f"  {f['name']} (ID: {f['id']})")


def main():
    config = load_config()
    base_path = config["workspace_path"]

    # Build folder mappings from config
    folder_mappings = []
    for course_name, course_config in config["courses"].items():
        if "drive_folder_name" in course_config:
            folder_mappings.append({
                "drive_name": course_config["drive_folder_name"],
                "local_name": course_config["local_folder_name"]
            })

    if not folder_mappings:
        print("No courses configured for Google Drive sync.")
        print("Add drive_folder_name to courses in config.json to enable sync.")
        return

    drive = GoogleDriveAPI()
    drive.authenticate()

    print("Syncing Google Drive folders to local storage...")
    print(f"Configured folders: {len(folder_mappings)}")

    success_count = 0
    for mapping in folder_mappings:
        drive_name = mapping["drive_name"]
        local_path = os.path.join(base_path, mapping["local_name"])

        if sync_folder(drive, drive_name, local_path):
            success_count += 1

    print(f"\nSync complete. {success_count}/{len(folder_mappings)} folders synced successfully.")

    if success_count < len(folder_mappings):
        list_available_folders(drive)


if __name__ == "__main__":
    main()
