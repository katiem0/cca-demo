---
description: "Use when preparing a Copilot Cloud Agent research-to-PR prompt for this demo repository."
---

Research the requested change in this repository first. Summarize the likely implementation plan,
call out test impact, and wait for approval before changing code. When approved, create a PR-sized
change with commits prefixed by the provided Jira ID.

Request: ${input:request:Describe the change to research}
Jira ID: ${input:jiraId:CCA-123}
