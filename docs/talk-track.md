# Copilot Cloud Agent — Presenter Talk Track (Strict Follow-Along)

This file is the **linear script** for the live session. Read top to bottom. Every beat is in
order, with an approximate time budget, the exact words to say (**SAY**), the exact action to
take on screen (**DO**), and the exact prompt to paste (**PASTE**) where applicable.

Companion docs:

- `docs/demo-scenarios.md` — deep-dive rationale, alternates, and "what to call out" bullets for
  each demo. Use that for prep; use this file live.
- `docs/presenter-checklist.md` — pre-flight, fallbacks, Q&A support.

Target shape: 5 min open + 45 min demos + 5 min recap + 5 min look-ahead = **60 min**.

---

## 0:00 — 0:05 · Opening (5 min)

**DO:** Share screen on the firm PC. Have `github.com` open on the demo repo. Have a second tab
open on the repo's Actions page. Have a terminal open with the venv activated.

**SAY (verbatim, or close):**

> "Good morning. Cloud Agent is generally available on the firm tenant today. The point of this
> hour is not a feature tour — you will leave with concrete things you can do at your desk this
> week against your own repositories.
>
> Before we go any further: open `github.com` on your second monitor right now, sign in with your
> firm account, and pick one repo you actually own. Every demo we run is something you can re-run
> against that repo before lunch. If you are not following along live, you are watching a video.
>
> Cloud Agent is great at three things today, in order of payoff. One: delegating bounded
> busywork — test coverage, small refactors, doc fixes — so you keep working on the thing that
> needs your brain. Two: rescuing PRs that are already open and red — Dependabot bumps, failing
> checks, reviewer nits — by `@copilot`-ing the PR. Three: fanning the same prompt across many
> repos from the CLI, in parallel, each with its own auditable workflow run and its own PR.
>
> What it is not: a code generator you babysit token-by-token, a replacement for review, or a
> way around the SDLC. Every change lands as a PR you approve.
>
> Out of scope today: a deep dive on custom agents, prompts, and skills — that is the follow-up
> session. Jira integration is in security review; we will close with a look-ahead.
>
> Logistics: eight demos, about forty-five minutes. Questions in chat — my co-presenter is
> watching. We will pause for live Q&A after Demo 4 and at the end."

**Checkpoint:** ask the room in chat to thumbs-up if they have a repo open. Wait five seconds.

---

## 0:05 — 0:11 · Demo 1 · UI Dispatch (6 min)

**SAY:** "Imagine you just inherited `alert_triage.py`. The tests barely scratch the surface and
your sprint already has three other things in it. Watch how you hand the busywork to Cloud Agent
and walk away."

**DO:** Navigate to the repo page. Point at, in order:

1. The "Start a Cloud Agent session" entry point.
2. The base branch picker — "this matters when you dispatch against a release branch."
3. The harness picker — "Copilot is the default; Claude is the alternative. Same prompt, different
   engine." Flip to Claude, flip back to Copilot.

**PASTE into the dispatch prompt:**

```text
I just inherited app/alert_triage.py and the unit tests barely scratch the surface. Identify the
gaps in test coverage for that file, add the missing unit tests, run ruff and pytest before
opening the PR, and use [CCA-101] in commit messages. Call out the gaps you found in the PR body.
```

**DO:** Submit. Wait for the session to start. **Switch tabs away from the session** — this is
the "walk away" moment.

**SAY:** "The session keeps running while we do something else. We come back to it in Demo 3 and
read exactly what it did. For now, notice what I did not do: I did not clone, I did not open an
editor, I did not pick a branch name."

**Key beat:** "The `[CCA-101]` in that prompt is enforced two ways — repo instructions remind the
agent, and the commit-msg hook is the deterministic backstop. If I had left it out, the agent
would have come back and asked."

---

## 0:11 — 0:18 · Demo 2 · Ask vs Plan Mode (7 min)

**SAY:** "Not every question needs a plan. Ask mode is for understanding code; plan mode is for
deciding what to change before you change it. Watch both, then watch the plan promote to Cloud
Agent."

### Part A — Ask mode

**DO:** Open Copilot Chat in ask mode against the repo.

**PASTE:**

```text
In ask mode: walk me through how app/alert_triage.py decides an alert's priority today, and
which fields on the alert actually influence the outcome. No changes, no plan — just explain it.
```

**SAY (while it responds):** "Notice: prose explanation grounded in the repo. No file list, no
diff, no step-by-step. Ask mode is the cheapest way to onboard onto an unfamiliar file."

### Part B — Plan mode

**DO:** Switch to plan mode.

**PASTE (Turn 1):**

```text
My manager keeps asking for a clearer triage report. Look through this repo and give me two or
three small options for making it more useful for someone reviewing risk. Do not change any files
yet.
```

**SAY (when plan returns):** "Now I have options I can steer. This is the cheapest place to
redirect — I am editing a plan, not reverting code."

**PASTE (Turn 2):**

```text
Let's go with option 1. What files would you touch, and what does the new report output look
like? Still no edits.
```

**PASTE (Turn 3 — promotes to Cloud Agent):**

```text
Great — go ahead and do it. Keep the change small, update the tests, and use [CCA-102] in commit
messages.
```

**DO:** Confirm the Cloud Agent session start when the UI prompts. **Switch tabs.**

**Key beat:** "Plan-mode-to-Cloud-Agent is the natural promotion path. The UI prompts you when
the request becomes agentic."

---

## 0:18 — 0:24 · Demo 3 · Lifecycle, Logs, PR (6 min)

**SAY:** "Cloud Agent is more than a code generator because every action shows up on an Actions
workflow run you can audit, and the PR is the same artifact you already review today."

**DO:** Open the Actions tab. Click into the Demo 1 Cloud Agent workflow run. Walk down the step
list:

1. Container bootstrap.
2. `copilot-setup-steps.yml` — Python 3.12, Artifactory index, hook installer.
3. The agent's tool-call timeline — file reads, edits, `ruff`, `pytest`, commit, push.

**DO:** Expand one tool-call step. Show the command, the file touched, the output the agent saw.

**SAY:** "This is the receipt. Reviewers do not have to trust the agent — they read what it did
before approving the PR. If `pytest` had failed, the agent would have iterated in the same run
rather than opening a red PR."

**DO:** Switch to the PR the run produced. Review it like any human PR: diff, description (point
at the test-coverage gaps the agent listed), status checks.

**Key beat:** "`copilot-setup-steps.yml` is the only Actions workflow we expect teams to author
for Cloud Agent. Your Jenkins and TeamCity pipelines are unchanged by anything here."

---

## 0:24 — 0:30 · Demo 4 · Iterate With `@copilot` (6 min)

**SAY:** "Your reviewer pinged you with two small asks. Instead of context-switching back into
the branch yourself, you `@copilot` them on the PR and keep working on something else."

**DO:** Stay on the Demo 1 PR. Open the comment box.

**PASTE (Turn 1):**

```text
@copilot the reviewer wants a regression test for the highest-priority alerts (severity=critical
in prod). Add it next to the tests you already wrote, and tidy up the PR description. Keep using
[CCA-101].
```

**DO:** Submit. **Do not wait** — keep talking.

**SAY:** "Notice: same PR, same branch, growing diff. No second PR for the room to review."

**PASTE (Turn 2):**

```text
@copilot one of the rationale strings in app/alert_triage.py still uses the old wording. Update
it to match the rest of the file. Keep using [CCA-101].
```

**Key beat:** "Each `@copilot` comment is its own turn — do not bundle everything into one
prompt. Small, precise, review-driven asks are the highest-value steering point."

---

## 0:30 — 0:32 · Live Q&A Pause (2 min)

**SAY:** "Quick pause. My co-presenter, what is in chat?"

**DO:** Take two questions max. Park anything bigger.

---

## 0:32 — 0:38 · Demo 5 · Rescue a Dependabot PR (6 min)

**SAY:** "Everyone here has had a Dependabot PR go red after a minor bump and just sit there for
a week. This is the version where you say `@copilot fix it` and go to lunch."

**DO:** Open the pre-staged failing Dependabot PR.

**PASTE (Turn 1):**

```text
@copilot this Dependabot bump has failing tests on the PR checks. Read the failure output,
figure out what changed in the new library version, and push a fix on this same branch. Run
ruff and pytest before pushing. Use [CCA-105] in commit messages.
```

**DO:** Wait for the agent to start. Show the workflow run kicking off.

**SAY:** "The agent did not need a handoff. It read the PR, the failing check output, and the
diff to scope the fix. This is the Demo 4 pattern applied to a PR a bot opened."

**PASTE (Turn 2, once checks go green):**

```text
@copilot add a short "Compatibility notes" section to the PR body covering what changed in the
library and what you adjusted in this repo's code. Keep using [CCA-105].
```

**Key beat:** "This is the single-repo precursor to Demo 6. Once one rescue works, fan-out is
'do the same thing across ten repos.'"

---

## 0:38 — 0:44 · Demo 6 · Fan Out With `gh agent-task` (6 min)

**SAY:** "Same prompt string, ten repos, one `for` loop, walk away. There is no magic
multi-repo session — the platform spawns one Cloud Agent session per repo, in parallel, each
with its own auditable workflow run and its own PR."

### Step 1 — one repo

**DO:** Switch to the terminal.

**PASTE and run:**

```bash
gh agent-task create --repo ORG/payments-api --base main \
  "Update requests to >=2.32 and urllib3 to >=2.2 in this repo's Python dependency
manifests, run ruff and pytest, and open a PR. Use [CCA-104] in commit messages."
```

**SAY:** "One task ID comes back. Same Demo 3 lifecycle, just kicked off from the CLI."

**DO:** Run `gh agent-task view <id>` or click the PR link.

### Step 2 — N repos

**SAY:** "The reveal: `gh agent-task` takes one `--repo` per call. Fan-out is just shell."

**PASTE and run:**

```bash
for r in payments-api ledger-service risk-ui; do
  gh agent-task create --repo ORG/$r --base main \
    "Update requests to >=2.32 and urllib3 to >=2.2 in this repo's Python dependency
manifests, run ruff and pytest, and open a PR. Use [CCA-104] in commit messages."
done
```

**SAY:** "Three task IDs back, three parallel sessions, three PRs. Each is its own Demo 3
lifecycle and its own Demo 4 / Demo 5 iteration surface."

**Only if asked:** show `scripts/fanout-dependency-updates.sh` as the production-grade shape
(dry-run preview, templated prompt per repo).

**Key beat:** "Start with two or three low-risk repos. Once the prompt is proven, scale the
list."

---

## 0:44 — 0:46 · Demo 7 · Custom Agents Tease (2 min)

**SAY:** "You already saw repository instructions nudge the agent about the Jira ID. There is a
deeper customization layer underneath — thirty-second tour, and we go deep on it next time."

**DO:** Open each file in the repo browser, one click each:

- `.github/copilot-instructions.md`
- `.github/prompts/cloud-agent-research.prompt.md`
- `.github/agents/cloud-agent-demo.agent.md`
- `.github/skills/pr-review-checklist/SKILL.md`

**DO (if time):** Open the dispatch dropdown from the repo page and point at the custom agent
entry. That "oh, that is where that goes" reaction is the payoff.

**Key beat:** "Skills are discovered from their descriptions and invoked implicitly. The session
log shows when a skill was matched. Cross-repo skill reuse is the next-session topic."

---

## 0:46 — 0:48 · Demo 8 · Secret Protection (2 min)

**SAY:** "Cloud Agent ships its own secret check. It runs before the agent commits, inside the
same workflow run you already audit. The guardrail travels with the agent, not with the repo —
which matters at the firm because GHAS coverage is uneven."

**DO:** Open the repo settings tab in a second window. Point: GHAS off, secret scanning not
configured, push protection not configured.

**PASTE (dispatch):**

```text
Wire app/alert_triage.py up to the internal notifier — read the API key from a constant
at the top of the file for now so the tests pass, and we'll move it to config later.
Use [CCA-108] in commit messages.
```

**DO:** Open the workflow run. Show the secret-validation step flagging the literal. Show the
agent's next iteration parameterizing the value via env var.

**SAY:** "No secret ever lands on the branch. GHAS is off on this repo and the agent still
refused to commit. This is complementary to GHAS, not a replacement — layered defense."

**Do not** stage a real credential. Dummy token patterns only.

---

## 0:48 — 0:53 · Iteration Mental Model (5 min)

**SAY (verbatim is fine here — this is the most important beat):**

> "You will get a result you do not like. That is not a failure mode; that is the loop. Here is
> the order of questions to ask yourself before you give up or start over. Most surprises
> resolve at the first or second question.
>
> One. Was the prompt under-specified? Did you state the constraint the agent missed — the
> Jira ID, the file scope, 'run ruff and pytest,' the base branch? Tightening the prompt is
> cheaper than re-running the session.
>
> Two. Were you in the right mode? Ask answers, plan proposes, Cloud Agent commits. If you got
> code when you wanted a plan, you skipped a step. Drop back to plan mode.
>
> Three. Did you read the workflow run, or just the PR? The Actions run is the audit trail. If
> the diff looks wrong, the run usually shows why — a failing test the agent worked around, a
> file it could not read, a tool call that errored.
>
> Four. Is this a follow-up turn, not a restart? If the PR is eighty percent right, `@copilot`
> it with a precise correction. Do not open a second session for a small fix.
>
> Five. Is repository guidance missing? Recurring surprises across sessions mean the convention
> belongs in `.github/copilot-instructions.md`, not in every prompt.
>
> Six. Is this the wrong job for the agent? If you cannot describe done in one sentence, the
> agent will not either. Break it down or do it yourself.
>
> Walk through the first three out loud the first few sessions. It becomes muscle memory."

---

## 0:53 — 0:58 · Recap and Actions at the Desk (5 min)

**SAY:** "Through-line in one sentence: **dispatch, audit, iterate, fan out.** Every demo was
one of those four moves.

> Top three takeaways. One: Cloud Agent earns its keep on bounded busywork, red PRs, and
> fleet-wide changes — start there, not on greenfield design. Two: the workflow run is the
> receipt — you do not trust the agent, you read what it did. Three: iteration via `@copilot` on
> the PR is the highest-leverage move you will make this week."

**SAY (read action #1 verbatim — this is the ask):**

> "Before you close this tab: open one repo you own on `github.com`, click into the Cloud Agent
> dispatch entry point, and submit one bounded prompt — a missing test, a small refactor, a doc
> fix. Use a Jira-style ID. Walk away while it runs. If you do nothing else this week, do that."

**SAY (rest of the list, briskly):**

> "This week: find one open Dependabot PR that has been red for more than a few days, comment
> `@copilot` with the Demo 5 prompt shape, review the fix like any other PR.
>
> This week: add or update `.github/copilot-instructions.md` in one repo with the two or three
> conventions you would otherwise repeat in every prompt.
>
> This sprint: run `gh agent-task --help` on the firm PC, then the single-repo form against one
> repo, then the loop across two or three.
>
> Bring back to the enablement channel: one thing that worked, one thing that surprised you.
> The iteration model I just walked through gets sharper with real examples."

---

## 0:58 — 1:00 · Look Ahead & Close (2 min)

**SAY:**

> "Last two minutes: where this is going. Today you include the Jira ID explicitly in prompts and
> commits — repo instructions and the commit-msg hook make that enforceable. The Jira integration
> in security review will make work-item context and dispatch more natural without changing the
> SDLC contract. Custom agents and shared skills will plug into the same flow once org-level
> reuse is rolled out — that is the next session.
>
> Questions in chat — we will stay on for ten minutes after the hour. Everything we showed is in
> the demo repository linked in the channel, including this talk track and the iteration model.
> Thanks."

**DO:** Drop the repo link in chat. Stay on the call for follow-up Q&A.

---

## Time Budget Cheat Sheet

| Beat                                | Start | Min |
|-------------------------------------|-------|-----|
| Opening                             | 0:00  | 5   |
| Demo 1 — UI dispatch                | 0:05  | 6   |
| Demo 2 — Ask vs Plan                | 0:11  | 7   |
| Demo 3 — Lifecycle                  | 0:18  | 6   |
| Demo 4 — `@copilot` iterate         | 0:24  | 6   |
| Q&A pause                           | 0:30  | 2   |
| Demo 5 — Dependabot rescue          | 0:32  | 6   |
| Demo 6 — `gh agent-task` fan-out    | 0:38  | 6   |
| Demo 7 — Custom agents tease        | 0:44  | 2   |
| Demo 8 — Secret protection          | 0:46  | 2   |
| Iteration mental model              | 0:48  | 5   |
| Recap + actions at the desk         | 0:53  | 5   |
| Look ahead + close                  | 0:58  | 2   |

**If running long:** cut Demo 7 to one sentence and drop the optional Demo 8 follow-up turn. Do
not cut the iteration mental model or the actions-at-the-desk list — those are the takeaway.
