# DOMANGCHA v4.1.1

This project runs on the DOMANGCHA project autonomous dev loop, and these rules take precedence over any global rules
The full rulebook is LOOP.md and is not loaded every session; follow the core below and read only the named section when it applies

- The only basis for resuming is .loop/PLAN.md; the session hook prints loop resume (if you do not see it: node scripts/loop.mjs resume)
- Every prompt is recorded by the hook as an instruction or an intervention, with the next action and the active policies (.loop/POLICY.md); follow it
- Questions, lookups, explanations and one-line typo fixes need no plan; anything that changes the repository gets a plan before code (LOOP.md section 1)
- Per item: loop start Ixx → implement inside the scope → self-audit a..h → loop pass or fail; never touch the next item before this one passes (LOOP.md section 2)
- When the plan must change, edit PLAN.md and run loop plan revise (LOOP.md section 2, step 5)
- After every item passes, run the final audit (LOOP.md section 4); heavy items follow section 5, policy promotion section 6
- An item that changes a user-facing screen or feature reads and applies LOOP.md section 8 (screen audit) and section 9 (completeness)
- Reporting: open with the loop card, name the stage and item id, announce start, middle and end of steps over 30 seconds, stop before approvals, never hide a failure
- The heavy rules (the DOMANGCHA harness) are in .claude/heavy/CEO.md; /ceo escalates the whole request to the harness
