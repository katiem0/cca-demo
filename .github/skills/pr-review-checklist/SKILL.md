---
name: pr-review-checklist
description: "Use when: reviewing Copilot Cloud Agent pull requests, checking PR readiness, validating demo PRs, or preparing Cloud Agent enablement examples."
---

# PR Review Checklist Skill

Use this skill to produce a short readiness review for Cloud Agent PRs in this demo repo.

## Checklist

1. Confirm the PR has a Jira-style identifier in the title, branch, or commit subject.
2. Confirm behavior changes include focused tests.
3. Confirm `ruff check .` and `pytest` were run or explain why not.
4. Confirm the PR body calls out setup, validation, and any remaining risk.
5. Flag broad rewrites, new external services, or secret-like values as demo blockers.

## Output Format

Use this concise shape:

```markdown
Cloud Agent PR readiness: pass/follow-up needed

- Jira/SDLC guardrail:
- Test coverage:
- Validation:
- Demo clarity:
- Follow-ups:
```
