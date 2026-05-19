# Repository Instructions for Copilot

This repository is a small Copilot Cloud Agent demo target. Keep changes focused,
easy to review, and suitable for a live enablement session.

## Commands

- Install dependencies: `python -m pip install -r requirements.txt -r requirements-dev.txt`
- Run tests: `pytest`
- Run lint: `ruff check .`
- Run the sample report: `python -m app.report`
- Install commit hooks: `./scripts/install-hooks.sh`

## Working Agreements

- Use Python 3.12 and keep the app dependency-light.
- Install runtime and dev dependencies from the firm Artifactory index when the Cloud Agent
  bootstraps the container (see `.github/workflows/copilot-setup-steps.yml`).
- Add or update tests for behavior changes.
- Prefer small PRs that show one Cloud Agent capability at a time.
- Commit subjects must start with a Jira-style ID such as `[CCA-123]`.
- If the Jira ID is missing from the user request, ask for it before creating commits.
- Do not add external services or secrets for demo scenarios.

## Demo-Friendly Behavior

- Explain setup or test failures in the pull request body.
- Mention which command verified the change.
- Keep generated examples understandable for first-time Cloud Agent users.
