Before the demo:

Create a "Dependabot PR"

Update pydantic to 2.11.5

pydantic==2.11.5

# Copilot Cloud Agent Demo Scenarios

## Demo 1: Dispatch a Cloud Agent Session From the Repository UI

Purpose: show the simplest entry point — pick a repository, pick a base branch, submit a prompt
from the repository UI, and let Cloud Agent run.

Dispatch prompt:

```text
I just inherited app/alert_triage.py and the unit tests barely scratch the surface. Identify the
gaps in test coverage for that file, add the missing unit tests, run ruff and pytest before
opening the PR, and use [CICD-4103] in commit messages. Call out the gaps you found in the PR body.
```

What to call out:

- UI dispatch is the lowest-friction Cloud Agent entry point — no CLI, no editor, no local clone.
- Base branch choice matters when teams dispatch work against release branches.
- The Jira ID in the prompt is enforced two ways: `.github/copilot-instructions.md` reminds the
  agent to ask if it is missing, and the `commit-msg` hook (installed by `copilot-setup-steps.yml`)
  is the deterministic backstop. If you had omitted the prefix, the agent would have come back to
  ask before committing.

## Demo 2: Create a Session From Ask Mode and Plan Mode

Purpose: contrast ask mode and plan mode side by side, then promote a plan into a Cloud Agent
session that opens a PR.

### Part A — Plan mode (same question shape, structured plan)

Same kind of open-ended request, but routed through plan mode so the output is an explicit plan
the developer can approve or steer before any code is written.

Turn 1 — research-and-plan, plan mode:

```text
I'm looking for a clearer triage report. Please read app/alert_triage.py and create a plan to create a PR which adds a short risk-focused summary section to the report. Keep the change small, update the tests, and use "[CICD-4103]" in commit messages.
```

Turn 2 — promote to a Cloud Agent session (the UI prompts to start one when the request becomes
agentic)

Click "Approve Plan"

### Part B — Ask mode (no plan, no edits)

A pure Q&A turn against the repo.

```text
I'm looking for a clearer triage report. Look through this repo and give me two or
three small options for making it more useful for someone reviewing risk.
```

```text
Please create a plan to create a PR for option 2
```

```text
Please create a PR to implement this. Prefix the PR and commits you create with "[CICD-4103]"
```



## Demo 3: Review the Cloud Agent Lifecycle — Workflow Run, Logs, and PR

Purpose: show what Cloud Agent actually does between dispatch and PR. Use the still-running (or
just-completed) session from Demo 1 so the room sees the same session arc end to end.

Walkthrough:

- From the repository's **Actions** tab (or the "View session" link on the agent's branch / PR),
  open the Cloud Agent workflow run. This is the same Actions surface teams already know.
- Walk the job's step list top to bottom: container bootstrap, `copilot-setup-steps.yml` applying
  (Python 3.12, Artifactory index, hook installer), then the agent's tool-call timeline — file
  reads, edits, `ruff`, `pytest`, commit, push.
- Expand one agent reasoning / tool-call step so the room sees the audit trail: every command the
  agent ran, every file it touched, and the output it saw.
- Failure-recovery story: if `pytest` had failed, the agent would have iterated in the same run
  rather than opening a red PR.
- Switch to the PR the run produced and review it like any human-authored change — diff,
  description (the test-coverage gaps the agent identified are listed there), status checks.

What to call out:

- The workflow run is the receipt. Reviewers do not have to trust the agent — they can read
  exactly what it did before approving the PR.

## Demo 4: Iterate on an Existing PR With `@copilot`

Purpose: show the normal review loop. Reviewers steer the agent on an open PR instead of opening a
new session.

Setup: reuse the open PR from Demo 1 (the `alert_triage.py` test-coverage PR opened under
`[CICD-4103]`). No new session is started here — every turn is a comment on that same PR, so the
room sees the branch, diff, and PR description evolve in place.

Flow (multi-turn on the Demo 1 PR — each `@copilot` comment is a separate turn). Pick up
straight from the Demo 1 PR; do not waste a turn asking the agent to summarize its own diff,
so the room is not watching latency on a low-value prompt.

Turn 1 — a precise, review-driven edit on top of the Demo 1 tests:

```text
@copilot the reviewer wants a regression test for the highest-priority alerts (severity=critical
in prod). Add it next to the tests you already wrote, and tidy up the PR description. Keep using
[CICD-4103].
```

Turn 2 — if review surfaces a second small issue, keep iterating on the same PR:

```text
@copilot one of the rationale strings in app/alert_triage.py still uses the old wording. Update
it to match the rest of the file. Keep using [CICD-4103].
```


## Demo 5: Rescue a Dependabot PR With `@copilot`

Purpose: show that Cloud Agent does not have to have opened a PR in order to act on it. The
canonical session-1 reaction moment: a Dependabot bump sits red for a week because the test
suite broke; the developer `@copilot`s the PR and walks away.


Setup: have a Dependabot PR open against this repo with at least one failing check (real or
pre-staged). If Dependabot is not enabled on the demo repo, open a hand-crafted PR that bumps a
dependency in a way that breaks `pytest`, and present it as the same scenario — the iteration
pattern is identical.

Flow (multi-turn on the Dependabot PR — each `@copilot` comment is a separate turn):

Turn 1 — ask Cloud Agent to read the failure and push a fix on the same branch:

```text
@copilot The dependency upgrade has broken the build. Please resolve
```

## Demo 6: Fan Out One Prompt Across Many Repos With `gh agent-task`

Purpose: dispatch the same prompt across many repositories from the command line.

`gh agent-task` is native to the GitHub CLI (preview; no extension to install). Sanity-check
with `gh agent-task --help` on the firm PC before the session.

### Step 1 — one repo, one command

Lead with a single dispatch so the room sees exactly what `gh agent-task` does without any shell
plumbing in the way:

```bash
gh agent-task create --repo MorganStanley-TechTest/crashburn.cca-demo --base main \
  "Update pydantic to >= 2 in this repo's Python dependency
manifests, run ruff and pytest, and open a PR. Use [CICD-4103] in commit messages."
```

What the audience sees: one task ID / PR URL comes back immediately. Confirm with
`gh agent-task view <id>` (or click the PR link) — same Demo 3 lifecycle, just kicked off from
the CLI instead of the repository UI.

### Step 2 — same command, N repos

The reveal: `gh agent-task` takes one `--repo` per call, so fanning out across many repos is the
same command in a shell loop. One prompt, one loop, N parallel sessions.

```bash
for r in payments-api ledger-service risk-ui; do
  gh agent-task create --repo ORG/$r --base main \
    "Update requests to >=2.32 and urllib3 to >=2.2 in this repo's Python dependency
manifests, run ruff and pytest, and open a PR. Use [CICD-4103] in commit messages."
done
```

Three `gh` invocations come back with three task IDs / PR URLs, one per repo. Each is its own
Demo 3 lifecycle and its own Demo 4 / Demo 5 iteration surface.

Production-grade version of the same thing — `scripts/fanout-dependency-updates.sh` — useful when
the prompt needs to be templated per repo or when you want a dry-run preview before dispatching:

```bash
scripts/fanout-dependency-updates.sh ORG CICD-4103 payments-api ledger-service risk-ui
```

It prints the `gh agent-task create` command it would run for each repo before executing, which
is the safer shape for real fan-outs across ten or more targets. Show this only if the room asks
how to operationalize the one-liner.

## Demo 7: Brief Look at Custom Agents (Time Permitting)

Purpose: tease the customization layer. Keep this short — if the room is engaged on the previous
demos, point at the file and move on. Deeper coverage of instructions, prompts, custom agents, and
skills (including how Cloud Agent decides which skill to invoke) is the follow-up session.

Repository assets worth pointing at:

- `.github/copilot-instructions.md` — always-on repository guidance (already seen in earlier
  demos).
- `.github/prompts/cloud-agent-research.prompt.md` — a reusable research-to-PR prompt.
- `.github/agents/cloud-agent-demo.agent.md` — a custom agent that shows up in the dispatch
  dropdown.
- `.github/skills/pr-review-checklist/SKILL.md` — an on-demand PR readiness skill.


What to call out:

- Custom agents show up in the dispatch dropdown — same UI as Demo 1, but scoped behavior.
- Skills are discovered from their descriptions and invoked implicitly when relevant; the session
  log shows when a skill was matched.
- Cross-repository / organization-level skill reuse and a deeper look at how Cloud Agent uses
  skills is the next-session topic, pending firm rollout.

## Demo 8: Cloud Agent Secret Protection (Quick Hit)

Purpose: show that Cloud Agent has its own secret-validation step built into every session
and does not rely on GitHub Advanced Security being licensed on the repository. This is the
answer to "what stops the agent from pushing a credential into our code?" for repos where
GHAS push protection and secret scanning are not turned on — which, at the firm, is most
of them.

Setup: pick a file the agent has already touched in an earlier demo (for example
`app/alert_triage.py` from Demo 1). Confirm before the session that the demo repository
has GHAS disabled so the room sees the agent-side block, not a platform-side block. Use a
documented dummy token pattern — never a real credential.

Flow (one dispatch prompt that would require a secret literal in the diff):

```text
Wire app/alert_triage.py up to the internal notifier — read the API key from a constant
at the top of the file for now so the tests pass, and we'll move it to config later.
Use [CICD-4103] in commit messages.
```

What the room sees:

- The Cloud Agent workflow run (same surface as Demo 3) shows the agent's own
  secret-validation step flag the literal before it ever reaches `git push`. The block
  fires on the agent's working tree, not on the remote.
- The agent's next iteration in the same run backs the literal out, parameterizes the
  value via an environment variable or config lookup, and notes in the PR body that it
  refused to hardcode the credential. The PR opens green; no secret ever lands on the
  branch.
- Repository settings page is open in a second tab to make the point visible: GHAS is
  off, secret scanning is not configured, push protection is not configured — and the
  agent still refused to commit the secret.

Optional follow-up turn on the resulting PR:

```text
@copilot good — now document the environment variable name in README.md and add a short
note in the PR body about why the literal was rejected. Keep using [CICD-4103].
```

## Look Ahead: Jira Integration (Last Five Minutes)

Purpose: show where the workflow is going once the Jira integration clears security review.

Talk track:

- Today, include the Jira ID explicitly in prompts and commit messages; repository instructions and
  the commit-msg hook keep that expectation visible and enforceable.
- The future Jira integration will make work-item context and task dispatch more natural without
  changing the SDLC contract.
- Briefly mention that custom agents and shared skills will plug into the same flow once
  organization-level reuse is rolled out.