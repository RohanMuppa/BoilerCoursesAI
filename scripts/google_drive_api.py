"""
Google Drive API Client
Supports reading, listing, and updating files in Google Drive.

Setup:
1. Go to https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable the Google Drive API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials.json and place in this directory
6. Install dependencies: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""

import io
import json
import os
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload


SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.file",
]

os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

TOKEN_FILE = "token.json"
TOKEN_ENV_VAR = "GOOGLE_DRIVE_TOKEN"
CREDENTIALS_FILE = "credentials.json"
CREDENTIALS_ENV_VAR = "GOOGLE_DRIVE_CREDENTIALS"


class GoogleDriveAPI:
    def __init__(
        self,
        credentials_file: str = CREDENTIALS_FILE,
        token_file: str = TOKEN_FILE,
        use_env_vars: bool = True,
    ):
        """
        Initialize Google Drive API client.

        Args:
            credentials_file: Path to OAuth credentials JSON file
            token_file: Path to store/load token JSON file
            use_env_vars: If True, check GOOGLE_DRIVE_TOKEN and GOOGLE_DRIVE_CREDENTIALS
                         environment variables first before falling back to files
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.use_env_vars = use_env_vars
        self.creds = None
        self.service = None

    def _load_token_from_env(self) -> Optional[Credentials]:
        """Load token from environment variable."""
        token_json = os.environ.get(TOKEN_ENV_VAR)
        if token_json:
            try:
                token_data = json.loads(token_json)
                return Credentials.from_authorized_user_info(token_data, SCOPES)
            except (json.JSONDecodeError, ValueError):
                return None
        return None

    def _load_credentials_from_env(self) -> Optional[dict]:
        """Load OAuth credentials from environment variable."""
        creds_json = os.environ.get(CREDENTIALS_ENV_VAR)
        if creds_json:
            try:
                return json.loads(creds_json)
            except json.JSONDecodeError:
                return None
        return None

    def authenticate(self) -> None:
        """
        Authenticate with Google Drive using OAuth 2.0.

        Checks environment variables first (if use_env_vars=True):
        - GOOGLE_DRIVE_TOKEN: JSON string of the OAuth token
        - GOOGLE_DRIVE_CREDENTIALS: JSON string of OAuth client credentials

        Falls back to files if env vars not set.
        """
        # Try loading token from env var first
        if self.use_env_vars:
            self.creds = self._load_token_from_env()

        # Fall back to token file
        if not self.creds and os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)

        # Refresh or get new token if needed
        if not self.creds or not self.creds.valid:
            refreshed = False
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                    refreshed = True
                except Exception:
                    print("Token refresh failed. Re-authenticating via browser...")
                    self.creds = None
            if not refreshed:
                # Try loading credentials from env var
                creds_data = None
                if self.use_env_vars:
                    creds_data = self._load_credentials_from_env()

                if creds_data:
                    flow = InstalledAppFlow.from_client_config(creds_data, SCOPES)
                elif os.path.exists(self.credentials_file):
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                else:
                    raise FileNotFoundError(
                        f"Missing credentials. Set {CREDENTIALS_ENV_VAR} env var or "
                        f"download {self.credentials_file} from Google Cloud Console."
                    )
                self.creds = flow.run_local_server(port=0)

            # Save token to file
            with open(self.token_file, "w") as token:
                token.write(self.creds.to_json())

            # Print token for env var setup
            print("\n" + "=" * 60)
            print("TOKEN FOR ENVIRONMENT VARIABLE")
            print("=" * 60)
            print(f"Set this as {TOKEN_ENV_VAR}:\n")
            print(self.creds.to_json())
            print("=" * 60 + "\n")

        self.service = build("drive", "v3", credentials=self.creds)

    def list_files(
        self,
        page_size: int = 10,
        query: Optional[str] = None,
        folder_id: Optional[str] = None,
    ) -> list[dict]:
        """
        List files in Google Drive.

        Args:
            page_size: Number of files to return (max 1000)
            query: Custom query string (see Drive API query syntax)
            folder_id: List files in a specific folder

        Returns:
            List of file metadata dictionaries
        """
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
        """
        Get metadata for a specific file.

        Args:
            file_id: The ID of the file

        Returns:
            File metadata dictionary
        """
        return (
            self.service.files()
            .get(fileId=file_id, fields="id, name, mimeType, size, modifiedTime, parents")
            .execute()
        )

    def read_file(self, file_id: str) -> bytes:
        """
        Read/download a file's content.

        Args:
            file_id: The ID of the file to read

        Returns:
            File content as bytes
        """
        request = self.service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)

        done = False
        while not done:
            _, done = downloader.next_chunk()

        file_stream.seek(0)
        return file_stream.read()

    def read_file_as_text(self, file_id: str, encoding: str = "utf-8") -> str:
        """
        Read a file's content as text.

        Args:
            file_id: The ID of the file to read
            encoding: Text encoding (default: utf-8)

        Returns:
            File content as string
        """
        return self.read_file(file_id).decode(encoding)

    def export_google_doc(self, file_id: str, mime_type: str = "text/plain") -> bytes:
        """
        Export a Google Docs/Sheets/Slides file to a different format.

        Args:
            file_id: The ID of the Google Doc
            mime_type: Export format (e.g., 'text/plain', 'application/pdf',
                      'text/csv', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')

        Returns:
            Exported content as bytes
        """
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
        """
        Update an existing file's content.

        Args:
            file_id: The ID of the file to update
            content: New file content (bytes or string)
            mime_type: MIME type of the content
            new_name: Optional new name for the file

        Returns:
            Updated file metadata
        """
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
        """
        Upload a new file to Google Drive.

        Args:
            file_path: Local path to the file
            name: Name for the file in Drive (defaults to local filename)
            folder_id: Optional folder ID to upload to
            mime_type: MIME type (auto-detected if not provided)

        Returns:
            Created file metadata
        """
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
        """
        Create a new file with content.

        Args:
            name: Name for the new file
            content: File content (bytes or string)
            mime_type: MIME type of the content
            folder_id: Optional folder ID to create in

        Returns:
            Created file metadata
        """
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
        """
        Delete a file from Google Drive.

        Args:
            file_id: The ID of the file to delete
        """
        self.service.files().delete(fileId=file_id).execute()

    def search_files(self, name_contains: str) -> list[dict]:
        """
        Search for files by name.

        Args:
            name_contains: Search string to match in file names

        Returns:
            List of matching files
        """
        query = f"name contains '{name_contains}'"
        return self.list_files(query=query, page_size=100)


# Example usage
if __name__ == "__main__":
    drive = GoogleDriveAPI()
    drive.authenticate()

    # List recent files
    print("Recent files:")
    files = drive.list_files(page_size=5)
    for f in files:
        print(f"  - {f['name']} ({f['id']})")

    # Example: Read a specific file (uncomment and add file ID)
    # file_id = "YOUR_FILE_ID_HERE"
    # content = drive.read_file_as_text(file_id)
    # print(f"File content:\n{content}")

    # Example: Export a Google Doc as plain text
    # doc_id = "YOUR_GOOGLE_DOC_ID"
    # text = drive.export_google_doc(doc_id, "text/plain").decode("utf-8")
    # print(f"Doc content:\n{text}")

    # Example: Update a file
    # drive.update_file(file_id, "New content here")

    # Example: Create a new file
    # new_file = drive.create_file("test.txt", "Hello, Google Drive!")
    # print(f"Created: {new_file['name']} ({new_file['id']})")
