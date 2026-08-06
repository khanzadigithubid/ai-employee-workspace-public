"""Read-only Google Workspace executive briefing.

This public example reads Calendar, Gmail, and Drive metadata and writes a
local Markdown report. It never creates, edits, or deletes Google data.

Before running, set GOOGLE_WORKSPACE_TOKEN_PATH to a local OAuth token file.
The token file must never be committed to Git.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build

SCOPES = (
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
)
DEFAULT_OUTPUT_DIR = Path("briefings")


def token_path() -> Path:
    configured = os.getenv("GOOGLE_WORKSPACE_TOKEN_PATH")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".config" / "google-workspace" / "token.json"


def load_credentials() -> Credentials:
    path = token_path()
    if not path.is_file():
        raise FileNotFoundError(
            f"OAuth token not found: {path}. "
            "Set GOOGLE_WORKSPACE_TOKEN_PATH to a local token.json file."
        )

    credentials = Credentials.from_authorized_user_file(str(path), SCOPES)
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    if not credentials.valid:
        raise RuntimeError("Google OAuth credentials are invalid or expired.")
    return credentials


def fetch_calendar_events(service: Resource, limit: int) -> list[dict[str, Any]]:
    now = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    response = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=limit,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return response.get("items", [])


def fetch_unread_messages(service: Resource, limit: int) -> list[dict[str, str]]:
    response = (
        service.users()
        .messages()
        .list(userId="me", q="is:unread", maxResults=limit)
        .execute()
    )
    summaries: list[dict[str, str]] = []
    for message in response.get("messages", []):
        details = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=["Subject", "From"],
            )
            .execute()
        )
        headers = {
            header["name"]: header["value"]
            for header in details.get("payload", {}).get("headers", [])
        }
        summaries.append(
            {
                "subject": headers.get("Subject", "No subject"),
                "from": headers.get("From", "Unknown sender"),
            }
        )
    return summaries


def fetch_recent_drive_files(service: Resource, limit: int) -> list[dict[str, str]]:
    response = (
        service.files()
        .list(
            pageSize=limit,
            fields="files(name,modifiedTime,webViewLink)",
            orderBy="modifiedTime desc",
        )
        .execute()
    )
    return response.get("files", [])


def render_markdown(
    events: list[dict[str, Any]],
    emails: list[dict[str, str]],
    files: list[dict[str, str]],
) -> str:
    generated = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    lines = ["# Executive Workspace Briefing", f"Generated: {generated}", ""]

    lines.extend(["## Upcoming Calendar Events", ""])
    if events:
        for event in events:
            start = event.get("start", {}).get(
                "dateTime", event.get("start", {}).get("date", "TBD")
            )
            lines.append(f"- **{event.get('summary', 'Untitled event')}** ({start})")
    else:
        lines.append("- No upcoming events found.")

    lines.extend(["", "## Unread Gmail Messages", ""])
    if emails:
        for email in emails:
            lines.append(
                f"- **{email['subject']}** — *from {email['from']}*"
            )
    else:
        lines.append("- No unread messages found.")

    lines.extend(["", "## Recently Modified Drive Files", ""])
    if files:
        for file in files:
            name = file.get("name", "Unnamed file")
            link = file.get("webViewLink", "#")
            lines.append(f"- [{name}]({link})")
    else:
        lines.append("- No recent files found.")

    return "\n".join(lines) + "\n"


def generate_briefing(output_dir: Path, limit: int) -> Path:
    credentials = load_credentials()
    calendar = build("calendar", "v3", credentials=credentials)
    gmail = build("gmail", "v1", credentials=credentials)
    drive = build("drive", "v3", credentials=credentials)

    report = render_markdown(
        fetch_calendar_events(calendar, limit),
        fetch_unread_messages(gmail, limit),
        fetch_recent_drive_files(drive, limit),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"briefing-{dt.date.today().isoformat()}.md"
    output_file.write_text(report, encoding="utf-8")
    return output_file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for generated Markdown reports (default: briefings)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum items per Google service (default: 5)",
    )
    args = parser.parse_args()
    if not 1 <= args.limit <= 50:
        parser.error("--limit must be between 1 and 50")

    output = generate_briefing(args.output_dir, args.limit)
    print(f"Briefing generated: {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
