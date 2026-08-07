# Google Workspace Executive Briefing

A read-only Python workflow that combines upcoming Google Calendar events, unread Gmail metadata, and recently modified Google Drive files into a local Markdown briefing.

## Safety model

- Uses only `calendar.readonly`, `gmail.readonly`, and `drive.readonly` scopes.
- Does not create, edit, delete, send, or mark-read Google data.
- Reads OAuth credentials from a path outside the repository.
- Writes reports locally to the selected output directory.
- Never commit `token.json`, OAuth client files, `.env` files, or generated reports containing personal data.

## Requirements

- Python 3.10+
- A Google Cloud OAuth desktop application
- A local authorized-user token with the read-only scopes listed above

Install dependencies from this directory:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Configure credentials

Set `GOOGLE_WORKSPACE_TOKEN_PATH` to the local authorized-user token JSON. Keep the file outside this repository.

Windows PowerShell:

```powershell
$env:GOOGLE_WORKSPACE_TOKEN_PATH = "$HOME\.config\google-workspace\token.json"
```

macOS/Linux:

```bash
export GOOGLE_WORKSPACE_TOKEN_PATH="$HOME/.config/google-workspace/token.json"
```

The token must be generated using these scopes:

- `https://www.googleapis.com/auth/calendar.readonly`
- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/drive.readonly`

## Run

From the repository root:

```bash
python automation/google_workspace_briefing.py --output-dir briefings
```

Useful options:

```bash
python automation/google_workspace_briefing.py --output-dir briefings --limit 10
```

The generated file is named `briefing-YYYY-MM-DD.md`. Review generated reports before sharing them because they may contain private email subjects, sender names, calendar titles, and Drive links.

## Scheduling

This repository includes a GitHub Actions workflow at `.github/workflows/briefing.yml`. It runs daily at 06:00 PKT and supports manual execution through the Actions tab.

For local use, you may use your operating system scheduler or an approved automation platform. Keep the job read-only and schedule it in the desired timezone. Do not publish scheduler configuration, OAuth tokens, or generated reports in this public repository.

## Troubleshooting

- **Token not found:** verify `GOOGLE_WORKSPACE_TOKEN_PATH` points to the local token JSON.
- **Invalid or expired credentials:** re-authorize the OAuth desktop application and replace the local token.
- **Access denied:** confirm the OAuth consent screen and the three read-only scopes.
- **No results:** the workflow only reports the first configured number of items and filters Gmail with `is:unread`.
