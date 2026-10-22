# Evidence Policy

A user-facing feature is done when its evidence run passes, not when code exists, a screen
renders, or a build is green. Rules a model can skip are replaced by adapters it has to pass.

Three steps, one flow:

1. Extract — to copy or benchmark a feature from another product, use REA (`rea` MCP server,
   `npx rea-agents setup`). Its findings are input, not proof about our product.
2. Build — native Claude Code: agents, Workflow, `/loop`, and a browser: the `ego-browser` skill when installed (run `ego-browser skill` first), otherwise Claude-in-Chrome; never Playwright while either is available.
3. Prove — `python3 ~/.domangcha/domangcha/engine.py evidence ...` in the project:
   - `evidence init` writes `.domangcha/evidence.json` once per project. Its commands run on this
     machine, so the person reviews them and runs `evidence trust` in their own terminal; any edit
     revokes trust. `evidence start` opens a run.
   - `evidence state enter <loading|empty|error|no-permission>`, capture the screen with
     that browser, `evidence record observation "<what you saw>" --source ego:<ref> --key state:<name>`
     (`chrome:<ref>` when Chrome was the browser),
     then `evidence state exit <name>`. A capture only counts inside the forced window.
   - Type a unique marker into the UI, save the browser's network entries to a file, and run
     `evidence trace <marker> --network <file> --label <flow>`: request → server log → stored row in one
     bundle. The marker is 6+ characters with a digit; the network file lives inside the project.
   - Tag every other claim: `observation` (needs `--source`), `derivation` (needs `--from` ids of
     observations), `inference` (needs `--basis`), `unknown` (what could not be established).
   - `evidence check` must pass; `evidence close` diffs against the previous run and flags any
     claim that went from observed to unknown as a regression.

Completion reports name the run id and quote `check`. An incomplete run is closed only with
`--accept-gaps "<reason>"`, which records the gap as an inference the user can see.
Screens implement the request as behaviour; they never restate it as copy.
