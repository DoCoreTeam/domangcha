---
name: ceo-agents
description: Logical DOMANGCHA role catalog backed by the canonical agent manifest.
---

# DOMANGCHA Agent Roles

`manifests/agents.json` is authoritative for IDs, groups, and ModelPolicy intent. `agents/dc-*.md` contains provider adapter prompts.

- PLANNER: DC-BIZ
- GENERATOR: DC-DEV-BE, DC-DEV-DB, DC-DEV-FE, DC-DEV-INT, DC-DEV-MOB, DC-DEV-OPS, DC-WRT

Review, security, QA, research, docs, and SEO use native agents: code-reviewer, security-reviewer, e2e-runner, Explore, doc-updater, seo-specialist, general-purpose.

Agent roles are optional Workflow or `/loop` steps selected by task need. Do not fan out in DIRECT. A writer cannot be the sole reviewer of meaningful implementation. Runtime adapters map roles to native capabilities; never assume Claude `Agent(...)` syntax exists elsewhere.
