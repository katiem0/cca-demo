#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  cat <<'USAGE'
Usage:
  scripts/fanout-dependency-updates.sh ORG JIRA_ID repo-a repo-b [repo-c ...]

Example dry run:
  scripts/fanout-dependency-updates.sh octo-org CCA-104 payments-api ledger-service risk-ui

This prints GitHub gh CLI commands for starting one Cloud Agent prompt session
per repository. It does not create GitHub Issues. Review the commands, then run
them manually or pipe them into a shell when you are ready.
USAGE
  exit 1
fi

org="$1"
jira_id="$2"
shift 2

for repo in "$@"; do
  prompt_file="/tmp/cca-dependency-prompts/$repo.md"
  prompt="$(cat <<BODY
Please update this repository's dependencies to current compatible versions.

Requirements:
- Keep the change small and dependency-focused.
- Update lockfiles or generated dependency metadata if present.
- Run the repository's documented lint and test commands.
- Create commits prefixed with [$jira_id].
- Open a PR with validation notes and any risk callouts.
BODY
)"

  printf 'mkdir -p /tmp/cca-dependency-prompts && printf %%s %q > %q && gh copilot task create --repo %q --base main --prompt-file %q\n' \
    "$prompt" "$prompt_file" "$org/$repo" "$prompt_file"
done
