---
name: ceo-agents
description: Logical DOMANGCHA role catalog backed by the canonical agent manifest.
---

# DOMANGCHA Agent Roles

`manifests/agents.json` is authoritative for IDs, groups, and ModelPolicy intent. `agents/dc-*.md` contains provider adapter prompts.

- PLANNER: DC-BIZ
- GENERATOR: DC-DEV-BE, DC-DEV-DB, DC-DEV-FE, DC-DEV-INT, DC-DEV-MOB, DC-DEV-OPS, DC-WRT

Review, security, QA, docs and SEO run on an independent reviewer subagent — `code-reviewer`, `security-reviewer`, `e2e-runner`, `doc-updater` or `seo-specialist` when installed (ECC ships them, also as `ecc:<name>`), otherwise native `general-purpose` in a context separate from the writer, briefed with the diff and the acceptance criteria; `Explore` for research. Only `general-purpose`, `Explore` and `Plan` ship with Claude Code; the named reviewers are optional, so resolve the first one present and never skip the review because a name is missing.

When ECC is installed (`DOMANGCHA_WITH_EXTRAS=1`, plugin `ecc:<name>`), these of its agents fit our roles; any one missing falls back as above:

| Need | ECC agent |
|---|---|
| review matching the diff's language | `typescript-reviewer`, `python-reviewer`, `react-reviewer`, `go-reviewer`, … |
| failures hidden as empty or zero | `silent-failure-hunter` |
| UI accessibility | `a11y-architect` |
| DC-DEV-DB work | `database-reviewer` |
| broken build | `build-error-resolver` |
| test gaps in a change | `tdd-guide`, `pr-test-analyzer` |

UI work uses the `design-taste-frontend` skill (taste-skill, installed by default, `DOMANGCHA_SKIP_TASTE=1` to skip) for art direction; `evidence.md` still decides completion.

Agent roles are optional Workflow or `/loop` steps selected by task need. Do not fan out in DIRECT. A writer cannot be the sole reviewer of meaningful implementation. Runtime adapters map roles to native capabilities; never assume Claude `Agent(...)` syntax exists elsewhere.
