<p align="center">
  <img src="assets/ai-engineering-workspace-banner.svg" alt="AI Engineering Workspace banner" width="100%">
</p>

<h1 align="center">AI Engineering Workspace</h1>

<p align="center">
  A sanitized public reference workspace for building reliable AI assistants, automations, and production systems with OpenClaw.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-6366f1.svg" alt="MIT License"></a>
  <a href="https://github.com/khanzadigithubid/ai-employee-workspace-public"><img src="https://img.shields.io/badge/status-public-22c55e.svg" alt="Public repository"></a>
  <a href="https://github.com/khanzadigithubid/ai-employee-workspace-public/actions/workflows/briefing.yml"><img src="https://github.com/khanzadigithubid/ai-employee-workspace-public/actions/workflows/briefing.yml/badge.svg?branch=main" alt="Generate Public Executive Briefing"></a>
  <a href="https://openclaw.ai/"><img src="https://img.shields.io/badge/powered%20by-OpenClaw-38bdf8.svg" alt="Powered by OpenClaw"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-blue.svg" alt="PRs Welcome"></a>
</p>

## Purpose

This repository demonstrates a clean, security-conscious structure for organizing an AI assistant's identity, operating principles, developer preferences, and reusable workspace documentation.

The original private workspace contains personal configuration, memory, schedules, and local integration files. Those private files are intentionally excluded from this public repository.

## Included

- `README.md` — project overview and public documentation
- `assets/ai-engineering-workspace-banner.svg` — repository branding banner
- `CONTRIBUTING.md` — guidelines for contributing
- `CHANGELOG.md` — version release tracking
- `automation/google_workspace_briefing.py` — read-only Google Workspace briefing workflow
- `automation/README.md` — setup, security, and scheduling guidance
- `automation/requirements.txt` — pinned dependency ranges
- `.github/workflows/briefing.yml` — scheduled GitHub Actions automation
- `.gitignore` — protection against credentials, tokens, local state, and runtime files
- `LICENSE` — MIT License for reuse and distribution

## Not Included

The following remain in the private backup repository:

- Personal profile and preferences
- Long-term memory and daily notes
- OAuth credentials and private token files
- Generated briefings and personal Workspace data
- Local schedules and runtime state
- Private OpenClaw configuration

## Automated GitHub Actions Workflow

The public repository includes `.github/workflows/briefing.yml`. It runs automatically every day at **06:00 AM Pakistan Standard Time (PKT)** and can also be started manually from **Actions -> Generate Public Executive Briefing -> Run workflow**.

### Workflow Process

1. GitHub starts a clean Python 3.12 Ubuntu runner.
2. Dependencies are installed from `automation/requirements.txt`.
3. OAuth values are loaded from encrypted GitHub Actions Repository Secrets.
4. The workflow refreshes the short-lived access token with the read-only refresh token.
5. Google Calendar, Gmail, and Drive metadata are fetched using read-only scopes.
6. A Markdown report is generated at `briefings/briefing-YYYY-MM-DD.md`.
7. GitHub Actions commits the generated report to the `main` branch.

### Required GitHub Secrets

Add these under **Settings -> Secrets and variables -> Actions -> Repository secrets**:

- `GOOGLE_CLIENT_ID` - OAuth client ID
- `GOOGLE_CLIENT_SECRET` - OAuth client secret
- `GOOGLE_ACCESS_TOKEN` - current Google access token
- `GOOGLE_REFRESH_TOKEN` - long-lived read-only refresh token

### Important Privacy Notice

This repository is public and the workflow has permission to commit generated reports. Briefings may contain private email subjects, sender names, calendar titles, and Drive links. Do not enable the scheduled workflow with a personal Google account unless you are comfortable publishing those reports. For private data, use the private backup repository or remove the commit step before running the workflow publicly.

## Security

Never commit API keys, OAuth tokens, passwords, private keys, `.env` files, session transcripts, personal memory, or generated private reports to a public repository. GitHub Actions Secrets are encrypted and are not visible in the repository, but generated output can still expose personal data. Review the workflow and every generated file before publishing.

## Contributing

Please check [CONTRIBUTING.md](CONTRIBUTING.md) before submitting pull requests.

## License

Released under the [MIT License](LICENSE).
