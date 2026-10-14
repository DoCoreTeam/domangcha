# DOMANGCHA v4.0.0 — LOOP project autonomous dev protocol

This file is the only working rulebook, loaded every session
In this project these rules take precedence over any global rules (~/.claude/CLAUDE.md)
Add project conventions to the appendix at the bottom only; leave the body alone
The heavy rules (the DOMANGCHA harness) live in .claude/heavy/CEO.md and are read only for items marked heavy

Slash commands are optional; plain natural language drives this protocol
The UserPromptSubmit hook records every prompt as an instruction or an intervention and prints the
next action together with the active policies, so following the hook output is enough

## 0 State and tools

- The only basis for resuming: .loop/PLAN.md — even after a context reset this file alone continues from the next item
- Accumulated policies: .loop/POLICY.md — repeated mistakes promoted by self-audit, checked line by line in every item audit
- Record CLI: node scripts/loop.mjs (written as loop below); instructions, interventions and implementations are stored in .loop/loop.db
- Recorded automatically by hooks: user prompts (instruction or intervention), file edits, session start, context compaction
- Recorded by the agent: loop plan new, plan check, plan confirm, plan revise, start, pass, fail, hold, final
- First action right after a session starts or the context is cleared: read the loop resume output (the hook prints it; run it yourself if you do not see it)

## 1 Loop 1 — plan before doing

On a new instruction, follow this order before touching code
An instruction given in plain language, with no slash command, follows the same procedure

Exceptions where no plan is written (answer directly and stop)
- Requests that do not change the repository: questions, lookups, explanations, summaries, reading code
- Changes so self-evident there is nothing to audit, such as fixing one typo
- When it is unclear whether a request qualifies, write the plan

1 Run loop resume to see whether a plan is active; if one is, treat the new instruction as an intervention and apply section 2
2 Run loop plan new --title "title" --instruction ins_xxxx --target vX.Y.Z (the ins id is in the hook output; from the current package.json version, raise minor for a feature and patch for a fix)
2a For a user-facing feature request, write the purpose chain from section 9 first and base the goal and the items on it
   purpose - entry path - task performed - sub-functions required - data and state - permissions and external dependencies - success result - failure and recovery path
   Sub-functions the purpose needs but the sentence never mentioned become items; assumptions that need a basis are separated out as things to confirm
3 Write the goal, out of scope, definition of done, references and items in .loop/PLAN.md
4 Revise until loop plan check passes
5 If plan_confirm is true, show the user a plan summary (item count, target version, out of scope), wait for their reply, and run loop plan confirm once they confirm
6 If plan_confirm is false, run loop plan confirm immediately

Writing items

- One item is a unit that a single self-audit can judge (at most 5 changed files; 1 to 4 audit criteria recommended)
- Scope: list the files or directories to change; mark new files "new"
- Audit criteria: only runnable commands with expected results, or observable conditions; never vague phrasing like "works well"
- Depends: preceding item ids, or "none"
- Mode: light by default; payments, authentication, permissions, data deletion, external APIs and secret handling are heavy
- Order: schema, server, screen, i18n, documentation by default, with dependencies deciding the real order
- An inserted item takes the previous number plus a letter (insert after I03 becomes I03a); never renumber existing items
- To drop an item, set its status to cancelled (reason) and keep the line

## 2 Loop 2 — implement an item and audit it

Repeat this per item and do not touch the next item until this one passes

1 Run loop start Ixx and treat the printed scope and audit criteria as the brief; in heavy mode read heavy_doc first
2 Implement, staying inside the scope
3 Run the 8-point self-audit
  a Scope match: the changed files in git status match the item scope; revert out-of-scope changes or record the reason in the summary
  b Static checks: cmd_typecheck passes, and cmd_lint passes if lint is configured
  c Item criteria: actually run or verify each criterion line and keep one line of evidence for each
  d Secrets and settings: no keys, tokens or passwords in the diff; new settings go to the database with UI management rather than new env vars (reusing existing env keys is fine)
  e i18n: every new user-facing string goes through an i18n key, with the default-language and English message files updated together
  f Side effects: nothing breaks another item's passing condition; re-run the related tests
  g Policy compliance: run loop policy check and compare every active rule against this change,
    record any breach with loop policy hit P00x --note "what you broke", fix it and compare again,
    never pass an item while a policy is broken
  h User-facing work: if this item changed a user-facing feature or screen, run both the 10 surface
    questions in section 8 and the completeness and verification checks in section 9, record which flows
    you actually exercised in a browser and what went unverified, and never record an unrun check as
    passed; if it changed neither, record one line saying so in the evidence
4 Decide
  - All satisfied: loop pass Ixx --summary "what you implemented" --notes "audit evidence + policy check result"; the CLI commits with a target-version-item-id message
  - Not satisfied but fixable inside the item: record loop fail Ixx --reason "reason", fix it, run loop start Ixx again and return to 3
  - Not satisfied and the plan itself must change: go to 5
5 Plan revision (the body of the loop)
  Triggers
  - A missing prerequisite: insert an item before the current one
  - Follow-up work discovered: append an item
  - The item is too large for a single audit: split it in two or more
  - The audit criteria are wrong or insufficient: fix the criteria
  - A user intervention changes the scope: add, edit or cancel items
  - Blocked by something external: loop hold Ixx --reason "reason"
  Procedure: edit the items in PLAN.md, run loop plan revise --level patch|minor --note "what and why" --ref audit:Ixx or --ref iv_xxxx, then continue section 2 against the revised plan
  Version rule: adding, editing or splitting items is patch; a user intervention that changes the goal or scope is minor
6 Limits (adjust with loop config)
  - max_audit_retries (default 3): past this many attempts on one item, loop hold it and ask the user to decide
  - max_plan_revisions_per_item (default 3): past this many revisions caused by one item, ask the user to decide

Handling interventions

- The hook records user prompts as iv_xxxx; the agent decides whether the intervention changes the plan
- If it does, apply it through the section 5 procedure (--ref iv_xxxx)
- If it does not, answer and continue; the CLI absorbs it when the item passes
- If it is a new feature unrelated to the current plan, propose a separate plan after this one finishes
- On "stop" or "abort", run loop hold or loop plan abort at once and record why

## 3 Context clearing and resuming

- Two clearing events: the tool's automatic compaction (the tool decides when) and the user's manual /clear
- Do not try to predict compaction; PLAN.md is current after every passing item, so nothing is lost whenever it happens
- When loop pass prints a checkpoint and a /clear suggestion, pass it to the user verbatim (shown every checkpoint_every passes)
- Resuming after a clear
  1 Read the loop resume output (the SessionStart hook prints it)
  2 If an item is active, its implementation state is unknown, so run loop start Ixx --force and redo the self-audit from section 2 step 3
  3 Otherwise start section 2 from the first pending item
  4 If the plan file and the database disagree, the plan file wins
- Never infer the earlier conversation on resume; take facts only from PLAN.md, git log and loop history

## 4 Final self-audit

After every item passes

1 Run cmd_typecheck, cmd_lint, cmd_test and cmd_build in full
2 Verify each line of the definition of done
3 Review the whole diff: git diff <start commit>..HEAD --stat (the start commit is in the PLAN.md header); no out-of-scope changes, no secrets, no hardcoded strings
4 Match items against results: the files in each item's scope actually exist or changed
5 Run loop policy check against the whole diff and confirm zero breaches
5a If this plan changed user-facing surfaces, apply the section 8 audit end to end on one representative user flow, then extend to the rest
5b If it changed a user-facing feature, check the 8 completion conditions in section 9 and move anything unconfirmed out of "done" and into the remaining limits
6 If this plan produced any policy hit, judge whether that rule worked and rewrite it if it did not
7 Record the result in the PLAN.md final-audit section (commands run and their results, the policy check result, and what you found)
8 Run loop final --result pass --summary "summary"; the CLI handles the completion commit, tag and archive
9 If something is unmet, record loop final --result fail --summary "reason", add remedial items with plan revise, and return to section 2

## 5 Heavy mode

- Heavy means applying the full DOMANGCHA harness (router, evidence gate, approval gates) to that item alone
- On start, an item in heavy mode reads heavy_doc (.claude/heavy/CEO.md by default) and applies those rules to that item only
- Record what the heavy rules produced in pass --notes as well
- Light items never read heavy_doc
- /ceo raises a whole request to the harness; if it is not installed, the loop offers to install it first

## 6 Policy self-learning

To stop repeating the same mistake, audit failures are promoted into rules that every later item checks

Promotion

1 When loop fail records policy_promote_after (default 2) failures on one item, the CLI flags it as a promotion candidate
2 Decide whether the cause is specific to this item or a general rule that would recur elsewhere
3 For a general rule: loop policy add --title "short title" --rule "what not to do and what to do instead" --origin audit:Ixx
4 For an item-specific mistake: fix it and do not promote a policy
5 A rule the user pointed out is promoted the same way, with --origin iv_xxxx

Writing a rule

- State an observable action; never "be careful" or "pay attention"
- Whether it was broken must be decidable from a diff or a command output
- One policy covers one thing; two things become two policies
- Example — bad: "follow i18n properly"; good: "adding a user-facing string means editing the ko and en message files in the same commit"

Rewriting and retiring

- A policy broken policy_rewrite_after (default 3) times is not written as something you can act on: retire it and write a more specific one
- When a structural change makes a rule meaningless: loop policy retire P00x --reason "reason"
- Growing the list is not the goal; delete rules that no longer earn their place

Injection paths

- Every prompt: the UserPromptSubmit hook prints the active policies with the directive
- Session start and after a context clear: included in the loop resume output
- Item audit: compared directly with loop policy check in section 2 step 3-g
- Three paths, so a context reset cannot lose them

## 7 Output and style

- Commit messages: item commits vX.Y.Z-Ixx: title, completion commit vX.Y.Z: plan title (the CLI writes both)
- Documents: terse lines, no decorative punctuation, no emoji, versions written v0.0.0
- Settings live in the database with UI management rather than new env vars
- This section is the style of what the agent itself produces; what the end user sees on screen is governed by section 8

## 8 Product surfaces

Applies only to items that change a user-facing surface; 3-h is this section's checklist
A surface is user-facing when someone who never read the repository will see it; an operator diagnostic view is held to behaviour, state and audit only

Development instructions are not product copy

- Implement the user's wording as behaviour; never move that sentence onto a heading, description, badge or menu
- "show everything at once" is an information-architecture change, not a subtitle; "fully automatic" is a trigger condition, not a badge
- "real time" is allowed only once the refresh mechanism exists; "merge the duplicate menus" is the merge itself, not a notice about it
- Banned on screen: "as requested", "we implemented", "we improved", "on this screen you can", "this system", "for your convenience"
- Rationale and technical explanation go in the work report and the documents, never in the UI

Copy

- Delete any string that does not report current state, direct the next action, state an input constraint, resolve an error, or disclose a consequence such as cost, permission or deletion
- Delete subtitles that repeat the heading, feature advertising, and instructions for the obvious
- Do not use "simple", "smart", "powerful", "innovative", "perfect", "at a glance", "seamless" or "optimal" as default modifiers; a real product name or a claim the code backs is the exception
- Brevity never removes input format, billing conditions, permission impact, deletion scope or recoverability

Names

- Adopt the domain vocabulary already in the repository and the ordinary convention of the category before inventing a word
- Menus name the thing or the job, buttons name the action that runs, states name the real state
- A consequential action names its object: cancel order, disconnect, delete account
- Replace buttons whose outcome is unreadable such as "get started", "proceed" or "manage" with the action; a dialog-dismissing "OK" is allowed
- Do not mix save, apply, register and done for one action; if two actions differ, define the difference
- One entity keeps one name across list, detail and settings
- Internal identifiers, API names, variable names, development phase names and a decorative AI prefix never appear in a user menu; real domain terms stay

Structure

- Do not derive menus from tables, service modules or build order; derive them from where a user starts and finishes a job
- Merge menus, cards and settings that serve one purpose, place sub-functions in the relevant detail view or tab, never route two differently named menus to one screen
- Do not force unrelated functions together
- No summary card, tab or section without real data or a real action behind it
- A plain list or form does not get a landing-page headline, promotional copy or a decorative badge
- The first screen leads with the work this user actually does and the information they decide on; feature-count showcases are prohibited

Behaviour

- Shipping a button or a menu means verifying UI, request, persistence or external effect, read back, UI refresh and the failure path
- Prohibited: a control that does nothing, a success message with no write behind it, a result that disappears on reload, fixed sample figures shown as live data, "completed" or "connected" or "synced" printed without checking the outcome, a menu whose only behaviour is a recurring "coming soon" notice, search filter sort download or notification affordances wired to nothing
- Unsupported functionality is not displayed by default; when the user must know it exists, state the limit, the reason and the alternative

States

- No data, load failure, loading and no permission are four different states
- Empty says what is absent and the next action, loading shows progress and blocks repeat submission, error says what did not complete and what to do, no permission says why and how to request access
- Show last refresh time and refresh failure where it matters, and report partial success as succeeded items and failed items separately
- Never disguise a failure as an empty list or a zero
- Stack traces, SQL, tokens and internal paths never reach a user screen; diagnostics go to the log
- Distinguish retryable actions from actions that risk duplicate processing, and preserve the user's input across an error wherever it can be preserved

Confirmations and notifications

- No confirmation on ordinary reads, navigation or saves; confirm deletion, payment, outbound sending and changes that are hard to undo
- A confirmation names the object, the effect and the action on its button; "are you sure?" alone is not a confirmation
- Report success once, after the result is confirmed, and never leave state the user must keep referring to only in a toast

Consistency and baseline usability

- Use the existing design system and shared components first
- Keep button placement, colour meaning, date currency and quantity formats, required-field marking and error display identical for identical functions
- Do not add icons, emoji, gradients, badges or animation that carry no meaning
- Icon-only controls carry an accessible name, state is never conveyed by colour alone, keyboard traversal and a visible focus indicator are preserved
- Long names, large numbers, other languages and small screens do not break layout or behaviour
- Show loading and disabled states with their reason where the reason is not obvious
- Back, reload and direct URL entry work, and returning from a detail view restores search, filter and page position where it can be

AI features

- AI involvement alone earns no badge, chat panel or explanatory paragraph; place it where it helps the actual job
- When basis, uncertainty or the need for review changes the user's decision, show it at that level, and never present an unverified result as settled fact
- Internal prompts, reasoning traces, agent names and development status messages stay off ordinary user screens; an operator diagnostic view is a separate labelled surface

Surface audit

Work through routes, menus, shared components, screen copy and the primary user flows, answering each question with evidence

1 Is a development instruction or an implementation report showing on screen?
2 Are there explanations, modifiers or badges carrying no role?
3 Does each menu name match what it actually does?
4 Is one function or one term duplicated or used inconsistently?
5 Does pressing a control reach a real result?
6 Is every displayed figure and state backed by real data?
7 Are empty, error, no-permission and loading distinguished?
8 Is a required cost, deletion or security disclosure missing?
9 Are navigation, input, small-screen and accessibility basics intact?
10 Did the fix break an existing flow?

- Fix one representative user flow end to end to confirm the standard, then extend to the rest; a first screen cleaned up is not a completed audit
- Copy changes do not justify restructuring, and deduplication preserves existing data, permissions and integrations
- Brand and marketing surfaces may carry deliberate visual ambition; working screens follow the restraint above

## 9 Feature completeness and verification

The other half of 3-h: section 8 covers what is visible, this covers whether it works
Code existing, a screen rendering and a build passing are not completion
Completion is a real user finishing the job in a browser, the result stored, surviving a reload and a fresh session, and recoverable when it fails

Purpose and flow

- Do not implement the request as a list of sentences; write this chain first
  purpose - entry path - task performed - sub-functions required - data and state - permissions and external dependencies - success result - failure and recovery path
- "Customer management" does not end at a customer list; it covers whichever of registration, detail, edit, delete or deactivate, search, duplicate handling, linked-work lookup and permission handling this project needs
- Separate stated requirement, fact confirmed in the existing system, gap you reasonably derived, and assumption needing confirmation; never implement an assumption as settled business policy
- Obviously necessary completion inside the requested scope is done without asking
- Money movement, permanent deletion, permission widening and outbound sending check existing precedent first, and with no precedent ask only the question needed

CRUD and lifecycle per managed entity

- For every entity this change touches, establish whether each is needed and whether it exists
  create (input, validation, duplicate check, persistence, confirmed result), read (list, detail, search, filter, sort, paging), update (load current values, validate, persist, reflect in related screens), delete (deletability conditions, blast radius, related data, reflected result), state transitions (approval, cancellation, closing, archiving, deactivation, restoration — whichever the domain needs)
- Do not bolt CRUD onto everything; transaction records, audit logs and external source data are handled read-only or through cancellation records and archiving, with the reason recorded
- Distinguish "not needed" from "not built"; when CRUD is partial, say which it is
- Check whether a delete breaks a reference, whether list and detail disagree after an edit, and whether a double submit creates the row twice

Paths to detail

- A list's primary item leads to its detail, a linked object's name to that object's detail, a count or total or statistic to the list or source data composing it, a notification to its subject or the task to act on, a history entry to the change and its subject
- Moving from a statistic to a list carries period, status and organisation, and the figure shown matches the result returned
- Do not make plain labels, units or decoration clickable; anything that looks clickable must do something meaningful, and an item that needs a detail view is not left as plain text
- Row click must not fight the row's checkbox or inline buttons, and links support open-in-new-tab and keyboard access

Detail screens

- Carry identity, principal attributes, current state, related data and available actions, and include change history when the job needs it
- A detail view showing only a name and a status is not done, and empty tabs or sections are not the fix either
- Choose page, side panel or modal by task complexity, navigation frequency and whether a direct link is needed; anything shared, bookmarked or returned to gets a stable URL
- Handle entry into a deleted subject, a nonexistent id, a subject the user may not access, and a stale notification link

UX design

- Placing components is not a UX review; these must be answerable against the running screen
  where does the user start, is the current subject and state immediately legible, is the most important next action obvious, must they carry information from another screen, are they retyping a value or bouncing between screens, can they confirm the result succeeded, can they recover or resume after a mistake or interruption, does it work with a lot of data and with none
- Preserve search, filter, sort, page and tab state where it belongs, and account for leaving mid-input, unsaved changes, double submission, long-running work and input lost to session expiry
- Before adding explanatory text, check whether structure, naming, defaults, placement or feedback solves it
- Make frequent work fast, put rare advanced functions where they are needed, and apply bulk actions and shortcuts only on demonstrated need

Design system

- Check for an existing design system and reuse it; with none, build the standard and shared components at the size this product needs
- Define consistently: colour and meaning (primary, secondary, danger, success, warning, disabled), type (size, weight, leading, heading-to-body hierarchy), spacing and layout (margins, measure, alignment, responsive breakpoints), components (button, input, select, table, tab, modal, panel, notification), states (default, hover, focus, selected, disabled, loading, error), data presentation (date, timezone, currency, quantity, unit, empty value)
- Put the definitions in tokens, shared components and shared formatters the code actually reuses, not only in a document
- Do not invent per-screen colours, sizes, modal behaviour or button order; the same role behaves the same way, and do not build a near-duplicate of a component that already solves it
- A design system is never a reason to introduce an unneeded framework or a large rewrite

Screen through to the stored result

- A feature is incomplete if any link is missing
  UI - event - API route - authorization and validation - service - database or job or external integration - result - UI refresh - failure and recovery
- Background work separates acceptance from completion, and its progress, failure and retry outcome reach the user
- Hiding a button in the frontend is not authorization; the server validates access to the target data and permission for the action
- Apply integrity and recovery measures that fit the job where concurrent edits, duplicate requests, partial failure or slow external responses are real, and do not attach the same machinery to every function

Looking for what the request left out

- Per request, check these and fill only the gaps that genuinely apply
  role-based access and data separation between organisations and users, required values and duplicates and invalid input and maximum length and boundary values, empty data and large data and long text and small screens, date and timezone and currency and decimals, agreement between search results and aggregate figures, the effect of editing or deleting linked data, external integration failure and timeout and session expiry, duplicate execution and concurrent edits and retry, the history and logs and recovery paths the job needs, query performance and excessive calls and avoidable cost, conflict with and regression of existing features
- This is not licence to add everything; separate a gap that blocks the purpose from feature expansion with no basis, and do not grow unrelated functions, settings or abstractions

Browser verification

- Code review, a successful API response and a green build do not substitute for UI verification; open the browser and click, type, navigate, save and re-read on the screen the user sees
- Run the scenarios that apply to what changed
  1 reach the feature through its normal entry path
  2 create or select the data it needs
  3 find it in the list and open its detail
  4 edit a value and confirm list and detail both reflect it
  5 reload and reconnect, and confirm the stored result survived
  6 check direct URL entry and the back button
  7 exercise the lifecycle that applies: delete, cancel, deactivate
  8 exercise invalid input, an empty result, a failure and a permission limit
  9 confirm related features are unaffected
  10 check the main viewport sizes for clipping, overlap, scroll and hit areas
- Read the console and network tab, but an absence of errors is not proof; confirm the data and state change the user expected actually happened
- Verify against test environments, accounts and data, and never delete production data, make a real payment or send externally in the name of verification
- When a browser or an integration is unreachable, run the verification that is possible and record exactly what went unverified; an unrun test is never reported as passed

Self-audit and re-verification

- After the first implementation, audit again for
  missing requirements, missing CRUD or detail or cross-screen links, inconsistent copy and naming and design, unnecessary steps and usability problems, false success indications and state mismatches, permission and data-integrity problems, missing error and failure and recovery handling, regression in existing features, unnecessary over-engineering
- Fix findings inside the current scope rather than filing a list, then re-run the scenario that exposed the problem and the flows directly affected
- When the same problem recurs, stop patching copy and exception handlers and find the cause in the data flow, the state management or the shared component
- Never claim perfection or absence of bugs

Completion conditions

All eight must hold; anything that does not is written down separately as a remaining limit

1 the requested feature and its necessary follow-on work are implemented
2 the required CRUD and detail paths are connected
3 what is stored and what is displayed agree
4 shared design, terminology and interaction standards are followed
5 the main success and failure scenarios were verified
6 existing flows affected by the change were checked
7 blocking defects found were fixed and re-verified
8 what could not be confirmed, and the remaining limits, are recorded separately

- Report only what changed, which flows were actually verified, what was found and fixed, and what limits remain
- Work blocked by an unreachable test environment or integration is not reported as done
- With many findings, resolve data corruption, permission errors and broken core flows first, then CRUD, detail links, state handling, UX and design consistency
- Split large work into verifiable units while keeping the whole checklist visible, and never describe improving some screens as completing the system
- Remaining work inside an already approved scope is not handed back as "shall I proceed?"; absent a real blocker, keep fixing and verifying

## Appendix — project conventions

- (add per project, e.g. package manager, test commands, design system INDEX path, supported languages)
