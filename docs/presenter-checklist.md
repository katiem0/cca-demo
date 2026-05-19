# Presenter Checklist

## Before the Session

- Confirm Copilot Cloud Agent access is enabled for the presenting account.
- Confirm both the Copilot and Claude harnesses are selectable on the firm tenant.
- Confirm the repository is visible to the target organization and branch protections are
  understood.
- Confirm Python 3.12 is the interpreter the Cloud Agent will pick up (the workflow pins it).
- Confirm `ARTIFACTORY_PYPI_INDEX` is set at the org / workflow level on the firm network.
- Run `python -m pip install -r requirements.txt -r requirements-dev.txt`.
- Run `ruff check .` and `pytest`.
- Run `./scripts/install-hooks.sh` if demonstrating local hook behavior.
- Prepare four Jira-style IDs for live prompts, for example `CCA-101` through `CCA-104`.

## During the Session

- Start with repository-level dispatch and base branch selection.
- Start Cloud Agent sessions from prompts only; do not use GitHub Issues as an entry point.
- Use Copilot as the default harness; switch to Claude once to show the harness picker.
- Show the session log briefly, then return to the PR review surface.
- Emphasize review, validation, and iteration rather than babysitting every step.
- Use `@copilot` on an existing PR for the review-loop demo.
- Treat skills and custom agents as a short preview unless questions pull the group deeper.

## Fallbacks

- If Cloud Agent dispatch is unavailable, walk through the prompts in `docs/demo-scenarios.md` and
  show the repository assets that support each behavior.
- If a live PR takes too long, switch to a pre-created PR and demonstrate review iteration.
- If image upload or Vision API behavior comes up, distinguish GitHub.com behavior from IDE preview
  feature availability.
