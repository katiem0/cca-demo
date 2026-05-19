# cca-demo-testing

Playground repository for validating Copilot Cloud Agent (CCA) demo scenarios
for an enablement session.

The sample application is intentionally tiny and is written in Python 3.12, the
language targeted for the firm demo. Cloud Agent sessions are dispatched only
through the Copilot or Claude harnesses, only from prompts or PR comments
(never GitHub Issues), and the Cloud Agent container bootstraps its Python
packages from the firm Artifactory index via
`.github/workflows/copilot-setup-steps.yml`.

Start with [docs/demo-scenarios.md](docs/demo-scenarios.md) for the run-of-show
and [docs/presenter-checklist.md](docs/presenter-checklist.md) for presenter prep.

## Layout

- `app/` — tiny sample service used as the change target.
- `tests/` — pytest suite (kept thin on purpose).
- `data/` — sample alerts used by the report command.
- `.github/copilot-instructions.md` — repo-level custom instructions.
- `.github/workflows/copilot-setup-steps.yml` — Cloud Agent environment setup. This is the
  only GitHub Actions workflow referenced during the demo; firm CI runs on Jenkins / TeamCity.
- `.github/prompts/` — reusable Cloud Agent research prompt.
- `.github/agents/` — focused custom agent for demo preparation.
- `.github/skills/pr-review-checklist/SKILL.md` — sample custom skill.
- `scripts/install-hooks.sh` — installs the commit-msg hook for Jira prefix.
- `scripts/fanout-dependency-updates.sh` — prints GitHub `gh` CLI prompt commands for
  dependency-update fan-out across repos.
- `docs/demo-scenarios.md` — the run-of-show. **Start here.**

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
pytest
python -m app.report
./scripts/install-hooks.sh   # optional: enables Jira-prefix commit-msg hook
```

You can also use `make setup`, `make lint`, `make test`, `make demo`, and
`make hooks`.

## Demo entry points

See [docs/demo-scenarios.md](docs/demo-scenarios.md) for the mapping of each
meeting bullet to a concrete prompt and expected agent behavior. Cloud Agent
sessions start from prompts or PR comments, not GitHub Issues.