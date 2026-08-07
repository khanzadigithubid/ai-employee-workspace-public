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

## GitHub Actions Automation

The public repository includes `.github/workflows/briefing.yml`. It runs every day at **06:00 AM Pakistan Standard Time (PKT)** using the UTC cron expression `0 1 * * *`. You can also start it manually from **Actions -> Generate Public Executive Briefing -> Run workflow**.

The workflow installs the dependencies, creates a temporary OAuth token file from GitHub Actions Secrets, refreshes the Google access token, fetches read-only Calendar, Gmail, and Drive metadata, and writes the report to `briefings/briefing-YYYY-MM-DD.md`.

### Required Repository Secrets

Configure these under **Settings -> Secrets and variables -> Actions -> Repository secrets**:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_ACCESS_TOKEN`
- `GOOGLE_REFRESH_TOKEN`

The workflow can commit generated reports to the public repository. Because reports may contain private Workspace metadata, use a private repository for personal data or remove the report commit step before enabling public automation.

For local use, you may use your operating system scheduler or an approved automation platform. Keep the job read-only and schedule it in the desired timezone. Do not publish scheduler configuration, OAuth tokens, or generated reports in this public repository.

## Troubleshooting

- **Token not found:** verify `GOOGLE_WORKSPACE_TOKEN_PATH` points to the local token JSON.
- **Invalid or expired credentials:** re-authorize the OAuth desktop application and replace the local token.
- **Access denied:** confirm the OAuth consent screen and the three read-only scopes.
- **No results:** the workflow only reports the first configured number of items and filters Gmail with `is:unread`.
