# DOMANGCHA Shared Core Policy

DOMANGCHA uses one adaptive execution authority: `domangcha/engine.py`.

- Normalize intent, then select the minimum reliable route: DIRECT, LOOP, or GRAPH.
- Deterministic invariants override probabilistic classification.
- Preserve state when escalating routes.
- A writer is not the sole reviewer of a meaningful implementation.
- Never claim completion without relevant executable validation.
- External, destructive, or irreversible effects require explicit authority.
- Report progress by default, in the user's language: the selected route and why, then progress
  through native surfaces — TodoWrite, Workflow phases, LOOP passes. Ask approval through
  AskUserQuestion before destructive or irreversible work. Never hide a stall or a failure.
- Do not re-implement what the runtime already provides: loops, graphs, checkpoints, memory,
  search, reviewers, and the browser are native. DOMANGCHA owns routing and evidence.
- A user-facing feature is complete only when `policies/evidence.md` passes: four forced states
  captured, one marker traced browser → server → database, every claim tagged by provenance.
