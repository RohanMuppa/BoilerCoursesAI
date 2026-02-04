"""
Google Drive API Client using Service Account Authentication
For server-to-server communication without user interaction.

Setup:
1. Go to https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable the Google Drive API
4. Create a Service Account (IAM & Admin > Service Accounts)
5. Create and download a JSON key for the service account
6. Save as service_account.json in this directory
7. Share Drive files/folders with the service account email
8. Install: pip install google-api-python-client google-auth
"""

import io
import os
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload


SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.file",
]

SERVICE_ACCOUNT_FILE = "service_account.json"


class GoogleDriveServiceAccount:
    def __init__(
        self,
        service_account_file: str = SERVICE_ACCOUNT_FILE,
        delegated_user: Optional[str] = None,
    ):
        """
        Initialize Google Drive API with service account.

        Args:
            service_account_file: Path to service account JSON key
            delegated_user: Optional email to impersonate (requires domain-wide delegation)
        """
        self.service_account_file = service_account_file
        self.delegated_user = delegated_user
        self.service = None

    def authenticate(self) -> None:
        """Authenticate using service account credentials."""
        if not os.path.exists(self.service_account_file):
            raise FileNotFoundError(
                f"Missing {self.service_account_file}. "
                "Download it from Google Cloud Console > IAM > Service Accounts."
            )

        creds = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=SCOPES
        )

        if self.delegated_user:
            creds = creds.with_subject(self.delegated_user)

        self.service = build("drive", "v3", credentials=creds)

    def list_files(
        self,
        page_size: int = 10,
        query: Optional[str] = None,
        folder_id: Optional[str] = None,
    ) -> list[dict]:
        """List files accessible to the service account."""
        if folder_id:
            query = f"'{folder_id}' in parents"

        results = (
            self.service.files()
            .list(
                pageSize=page_size,
                fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)",
                q=query,
            )
            .execute()
        )
        return results.get("files", [])

    def get_file_metadata(self, file_id: str) -> dict:
        """Get metadata for a specific file."""
        return (
            self.service.files()
            .get(fileId=file_id, fields="id, name, mimeType, size, modifiedTime, parents")
            .execute()
        )

    def read_file(self, file_id: str) -> bytes:
        """Read/download a file's content."""
        request = self.service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        file_stream.seek(0)
        return file_stream.read()

    def read_file_as_text(self, file_id: str, encoding: str = "utf-8") -> str:
        """Read a file's content as text."""
        return self.read_file(file_id).decode(encoding)

    def export_google_doc(self, file_id: str, mime_type: str = "text/plain") -> bytes:
        """Export a Google Docs/Sheets/Slides file."""
        request = self.service.files().export_media(fileId=file_id, mimeType=mime_type)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        file_stream.seek(0)
        return file_stream.read()

    def update_file(
        self,
        file_id: str,
        content: bytes | str,
        mime_type: str = "text/plain",
        new_name: Optional[str] = None,
    ) -> dict:
        """Update an existing file's content."""
        if isinstance(content, str):
            content = content.encode("utf-8")

        media = MediaIoBaseUpload(io.BytesIO(content), mimetype=mime_type, resumable=True)

        file_metadata = {}
        if new_name:
            file_metadata["name"] = new_name

        return (
            self.service.files()
            .update(
                fileId=file_id,
                body=file_metadata if file_metadata else None,
                media_body=media,
                fields="id, name, mimeType, modifiedTime",
            )
            .execute()
        )

    def upload_file(
        self,
        file_path: str,
        name: Optional[str] = None,
        folder_id: Optional[str] = None,
        mime_type: Optional[str] = None,
    ) -> dict:
        """Upload a new file to Google Drive."""
        file_metadata = {"name": name or os.path.basename(file_path)}

        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        return (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id, name, mimeType")
            .execute()
        )

    def create_file(
        self,
        name: str,
        content: bytes | str,
        mime_type: str = "text/plain",
        folder_id: Optional[str] = None,
    ) -> dict:
        """Create a new file with content."""
        if isinstance(content, str):
            content = content.encode("utf-8")

        file_metadata = {"name": name}
        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaIoBaseUpload(io.BytesIO(content), mimetype=mime_type, resumable=True)

        return (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id, name, mimeType")
            .execute()
        )

    def delete_file(self, file_id: str) -> None:
        """Delete a file from Google Drive."""
        self.service.files().delete(fileId=file_id).execute()

    def search_files(self, name_contains: str) -> list[dict]:
        """Search for files by name."""
        query = f"name contains '{name_contains}'"
        return self.list_files(query=query, page_size=100)


if __name__ == "__main__":
    drive = GoogleDriveServiceAccount()
    drive.authenticate()

    print("Files accessible to service account:")
    files = drive.list_files(page_size=5)
    for f in files:
        print(f"  - {f['name']} ({f['id']})")
