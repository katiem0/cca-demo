# Copilot Cloud Agent Demo Scenarios

This runbook showcases
concrete repository assets and prompts. Target shape: five minutes of framing slides, forty-five to
fifty minutes of live demo on the firm PC, and a five-minute look ahead to Jira integration.

Guardrails for the session:

- All Cloud Agent sessions start from either a repository / user-level prompt or a PR comment.
  GitHub Issues are not used at the firm and are not part of any demo path.
- Only the Copilot and Claude coding agent harnesses are in scope. Show the harness picker, and
  use Copilot as the default; switch to Claude at most once to illustrate that the same prompt can
  be routed to either harness against the same repository.
- The sample application is Python 3.12. Python has mass appeal at the firm and is the language
  whose Cloud Agent container bootstrap works cleanly with `copilot-setup-steps.yml` pulling
  packages from the firm Artifactory index.
- Most teams run CI on Jenkins or TeamCity, not GitHub Actions. The only GitHub Actions workflow
  worth showing live is `.github/workflows/copilot-setup-steps.yml`, and only to demonstrate how
  the Cloud Agent's container is prepared.
- Steering mid-session is mentioned in one sentence, not demoed. Encourage attendees to set the
  prompt and let the agent run.


## Demo 1: Dispatch a Cloud Agent Session From the Repository UI

Purpose: show the simplest entry point — pick a repository, pick a base branch, submit a prompt
from the repository UI, and let Cloud Agent run.

Framing for the room: "Imagine you just inherited `alert_triage.py`. The tests barely scratch the
surface and your sprint already has three other things in it. Here is how you delegate the busywork
to Cloud Agent and go grab a coffee."

What to point at on screen before submitting the prompt:

- The "Start a Cloud Agent session" entry point on the repository page.
- The base branch picker — call out that this matters when teams dispatch against release branches.
- The harness picker. Copilot is the default; Claude is the alternative. Same prompt, different
  engine — flip it once for the reaction, then stay on Copilot.

Dispatch prompt:

```text
I just inherited app/alert_triage.py and the unit tests barely scratch the surface. Identify the
gaps in test coverage for that file, add the missing unit tests, run ruff and pytest before
opening the PR, and use [CCA-101] in commit messages. Call out the gaps you found in the PR body.
```

This is the "walk away" moment. Pause the talk track, switch browser tabs, point out that the
session keeps running while you do something else — Demo 3 is where we come back and inspect what
it actually did.

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

Framing for the room: "Not every question needs a plan. Ask mode is for understanding the code;
plan mode is for deciding what to change before you change it. Show both, then promote the plan
to Cloud Agent."

### Part A — Ask mode (no plan, no edits)

A pure Q&A turn against the repo. The agent reads files and answers; it does not produce a
structured plan or propose edits.

```text
In ask mode: walk me through how app/alert_triage.py decides an alert's priority today, and
which fields on the alert actually influence the outcome. No changes, no plan — just explain it.
```

What the room should notice: the response is prose explanation grounded in the repo. No file
list, no proposed diff, no "step 1 / step 2." Ask mode is the cheapest way to onboard onto an
unfamiliar file.

### Part B — Plan mode (same question shape, structured plan)

Same kind of open-ended request, but routed through plan mode so the output is an explicit plan
the developer can approve or steer before any code is written.

Turn 1 — research-and-plan, plan mode:

```text
My manager keeps asking for a clearer triage report. Look through this repo and give me two or
three small options for making it more useful for someone reviewing risk. Do not change any files
yet.
```

Turn 2 — narrow the plan based on what plan mode returned:

```text
Let's go with option 1. What files would you touch, and what does the new report output look
like? Still no edits.
```

Turn 3 — promote to a Cloud Agent session (the UI prompts to start one when the request becomes
agentic):

```text
Great — go ahead and do it. Keep the change small, update the tests, and use [CCA-102] in commit
messages.
```

What to call out:

- Ask mode vs plan mode is the key contrast: same surface, different output shape. Ask mode
  answers; plan mode proposes ordered steps and file targets you can approve.
- Plan mode is the cheapest place to steer — you are editing a plan, not reverting code.
- The user-level entry point lets a developer pick any repository they have access to from a
  single starting page.
- Plan mode → Cloud Agent is a natural promotion point; the UI prompts to start a session when
  the request becomes agentic.
- The plan-approval moment is the cheapest place to steer before any code exists.

## Demo 3: Review the Cloud Agent Lifecycle — Workflow Run, Logs, and PR

Purpose: show what Cloud Agent actually does between dispatch and PR. Use the still-running (or
just-completed) session from Demo 1 so the room sees the same session arc end to end.

Framing for the room: "The reason this is more than a code generator: every action the agent takes
shows up on an Actions workflow run you can audit, and the PR at the end is the same artifact you
already review today."

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
- `copilot-setup-steps.yml` is the only GitHub Actions file we expect teams to author for Cloud
  Agent. Firm CI on Jenkins / TeamCity is unchanged by anything shown here.
- Once you have seen the session log once, ignore it — the PR is the artifact developers will
  actually live with.

## Demo 4: Iterate on an Existing PR With `@copilot`

Purpose: show the normal review loop. Reviewers steer the agent on an open PR instead of opening a
new session.

Framing for the room: "Your reviewer pinged you with two small asks. Instead of context-switching
back into the branch yourself, you just `@copilot` them on the PR and keep working on something
else."

Setup: reuse the open PR from Demo 1 (the `alert_triage.py` test-coverage PR opened under
`[CCA-101]`). No new session is started here — every turn is a comment on that same PR, so the
room sees the branch, diff, and PR description evolve in place.

Flow (multi-turn on the Demo 1 PR — each `@copilot` comment is a separate turn). Pick up
straight from the Demo 1 PR; do not waste a turn asking the agent to summarize its own diff,
so the room is not watching latency on a low-value prompt.

Turn 1 — a precise, review-driven edit on top of the Demo 1 tests:

```text
@copilot the reviewer wants a regression test for the highest-priority alerts (severity=critical
in prod). Add it next to the tests you already wrote, and tidy up the PR description. Keep using
[CCA-101].
```

Turn 2 — if review surfaces a second small issue, keep iterating on the same PR:

```text
@copilot one of the rationale strings in app/alert_triage.py still uses the old wording. Update
it to match the rest of the file. Keep using [CCA-101].
```

What to call out:

- This is the highest-value steering point for reviewers: small, precise, review-driven asks.
- The agent updates the existing PR (the one from Demo 1) instead of opening a second one — same
  branch, same Jira ID, growing diff.
- Each `@copilot` comment is its own conversation turn — you do not have to bundle everything into
  the first prompt.
- The same repository instructions apply on follow-up turns, so the Jira-ID expectation still holds.

## Demo 5: Rescue a Dependabot PR With `@copilot`

Purpose: show that Cloud Agent does not have to have opened a PR in order to act on it. The
canonical session-1 reaction moment: a Dependabot bump sits red for a week because the test
suite broke; the developer `@copilot`s the PR and walks away.

Framing for the room: "Everyone here has had a Dependabot PR go red after a minor version bump
and just sit there. This is the version where you say `@copilot fix it` and go to lunch."

Setup: have a Dependabot PR open against this repo with at least one failing check (real or
pre-staged). If Dependabot is not enabled on the demo repo, open a hand-crafted PR that bumps a
dependency in a way that breaks `pytest`, and present it as the same scenario — the iteration
pattern is identical.

Flow (multi-turn on the Dependabot PR — each `@copilot` comment is a separate turn):

Turn 1 — ask Cloud Agent to read the failure and push a fix on the same branch:

```text
@copilot this Dependabot bump has failing tests on the PR checks. Read the failure output,
figure out what changed in the new library version, and push a fix on this same branch. Run
ruff and pytest before pushing. Use [CCA-105] in commit messages.
```

Turn 2 — once the checks go green, ask for a one-line compatibility note in the PR body:

```text
@copilot add a short "Compatibility notes" section to the PR body covering what changed in the
library and what you adjusted in this repo's code. Keep using [CCA-105].
```

What to call out:

- `@copilot` works on any PR — including ones Cloud Agent did not open. The agent did not need
  context handoff; it read the PR, the failing check output, and the diff to scope the fix.
- When Cloud Agent touches dependency manifests it consults the GitHub advisory database; that
  surface shows up on the workflow run from the Demo 3 lifecycle.
- This is the same `@copilot` iteration pattern as Demo 4, just applied to a PR a bot opened.
- This is the single-repo precursor to Demo 6 — once one Dependabot rescue works, fan-out is
  "do the same thing across ten repos."

## Demo 6: Fan Out One Prompt Across Many Repos With `gh agent-task`

Purpose: dispatch the same prompt across many repositories from the command line.

Framing for the room: "Same prompt string, ten repos, one `for` loop, then walk away. Demo 5
was one Dependabot PR; this is the same pattern across the whole fleet. There is no magic single
session — the platform spawns one Cloud Agent session per repo, in parallel, each with its own
auditable workflow run like Demo 3 and its own PR you can iterate on like Demo 4 or Demo 5."

`gh agent-task` is native to the GitHub CLI (preview; no extension to install). Sanity-check
with `gh agent-task --help` on the firm PC before the session.

### Step 1 — one repo, one command

Lead with a single dispatch so the room sees exactly what `gh agent-task` does without any shell
plumbing in the way:

```bash
gh agent-task create --repo ORG/payments-api --base main \
  "Update requests to >=2.32 and urllib3 to >=2.2 in this repo's Python dependency
manifests, run ruff and pytest, and open a PR. Use [CCA-104] in commit messages."
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
manifests, run ruff and pytest, and open a PR. Use [CCA-104] in commit messages."
done
```

Three `gh` invocations come back with three task IDs / PR URLs, one per repo. Each is its own
Demo 3 lifecycle and its own Demo 4 / Demo 5 iteration surface.

Production-grade version of the same thing — `scripts/fanout-dependency-updates.sh` — useful when
the prompt needs to be templated per repo or when you want a dry-run preview before dispatching:

```bash
scripts/fanout-dependency-updates.sh ORG CCA-104 payments-api ledger-service risk-ui
```

It prints the `gh agent-task create` command it would run for each repo before executing, which
is the safer shape for real fan-outs across ten or more targets. Show this only if the room asks
how to operationalize the one-liner.

What to call out:

- Lead with the single-repo invocation. The shell loop is the reveal, not the headline — the
  room first sees one clean command, then realizes it scales by repetition.
- Cloud Agent has no native multi-repo dispatch — `gh agent-task` takes one `--repo` per call,
  so fan-out is just shell.
- `gh agent-task` is the native Cloud Agent dispatcher in `gh` (preview); `gh copilot`
  (suggest / explain) is a separate extension and is not what creates sessions.
- Each spawned session has its own workflow run (Demo 3) and its own PR (Demo 4); the loop only
  kicks off the first turn in each repo. Use `gh agent-task list` / `view` to follow them.
- This path must not create or assign GitHub Issues.
- Start with two or three low-risk repositories, then scale the list once the prompt is proven.

## Demo 7: Brief Look at Custom Agents (Time Permitting)

Purpose: tease the customization layer. Keep this short — if the room is engaged on the previous
demos, point at the file and move on. Deeper coverage of instructions, prompts, custom agents, and
skills (including how Cloud Agent decides which skill to invoke) is the follow-up session.

Framing for the room: "You already saw repository instructions nudge Copilot about the Jira ID.
There is a deeper customization layer underneath — here is the thirty-second tour, and we will go
deep on it next time."

Repository assets worth pointing at:

- `.github/copilot-instructions.md` — always-on repository guidance (already seen in earlier
  demos).
- `.github/prompts/cloud-agent-research.prompt.md` — a reusable research-to-PR prompt.
- `.github/agents/cloud-agent-demo.agent.md` — a custom agent that shows up in the dispatch
  dropdown.
- `.github/skills/pr-review-checklist/SKILL.md` — an on-demand PR readiness skill.

Optional live moment if time allows: open the dispatch dropdown from a repository page and point
at the custom agent entry — that "oh, that is where that goes" reaction is the cheapest payoff in
this slot.

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

Framing for the room: "Cloud Agent ships its own secret check —
it runs before the agent commits, inside the same workflow run you already audit. The
guardrail travels with the agent, not with the repo."

Setup: pick a file the agent has already touched in an earlier demo (for example
`app/alert_triage.py` from Demo 1). Confirm before the session that the demo repository
has GHAS disabled so the room sees the agent-side block, not a platform-side block. Use a
documented dummy token pattern — never a real credential.

Flow (one dispatch prompt that would require a secret literal in the diff):

```text
Wire app/alert_triage.py up to the internal notifier — read the API key from a constant
at the top of the file for now so the tests pass, and we'll move it to config later.
Use [CCA-108] in commit messages.
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
note in the PR body about why the literal was rejected. Keep using [CCA-108].
```

What to call out:

- Cloud Agent's secret validation is part of the agent harness, not a repository feature.
  It runs on every Cloud Agent session regardless of whether GHAS is licensed on that
  repo, which matters at the firm where GHAS coverage is uneven.
- The workflow run is the audit trail: the rejected literal, the agent's reasoning, and
  the remediation commit are all in the same log reviewers already read in Demo 3.
- This is complementary to — not a replacement for — any future GHAS rollout. If push
  protection is later enabled on a repo, the agent's check fires first and the platform
  check is the backstop. Layered defense, no behavior change for developers.
- Keep this beat to thirty to sixty seconds. The point is reassurance for security
  stakeholders in the room, not a deep architectural walk-through.
- Do not stage a real credential for the demo. Use a documented dummy token format so
  the block is deterministic and safe to run on the firm PC.

## Look Ahead: Jira Integration (Last Five Minutes)

Purpose: show where the workflow is going once the Jira integration clears security review.

Talk track:

- Today, include the Jira ID explicitly in prompts and commit messages; repository instructions and
  the commit-msg hook keep that expectation visible and enforceable.
- The future Jira integration will make work-item context and task dispatch more natural without
  changing the SDLC contract.
- Briefly mention that custom agents and shared skills will plug into the same flow once
  organization-level reuse is rolled out.
