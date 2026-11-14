# Experimental protocol v0.1 (2026-11-14)

## Question

At fixed task requirements and model/tool configuration, how reliably can a **single** AI coding agent deliver completed software tasks, and what compute usage, time, and human supervision are required?

This is the **production baseline**, not yet a test of whether AI agents need credit or autonomous banking.

## Unit of observation

One agent attempt at one frozen task under one configuration, evaluated without human modification. Each attempt uses a fresh workspace; never let an agent reuse a previously completed task solution.

## Tasks

| ID | Skill under test | Key check |
|----|------------------|-----------|
| csv_export | Data format correctness | Escaping, missing values, ordering |
| usage_billing | Compute accounting | Cached token treatment, exact money math |
| rate_limiter | Stateful service logic | Window boundaries and rejection accounting |
| transfer_ledger | Financial transaction correctness | Idempotency and overdraft prevention |
| capacity_scheduler | Resource allocation | Capacity, cost minimization, deterministic ties |
| webhook_reconciliation | Asynchronous systems | Duplicate/out-of-order events and conflicts |

These six synthetic tasks are convenient for calibration, **not representative** of all real software projects and not evidence of actual customer willingness to pay. Some may be present in model training data; a later study should include newly written, private, independently valued tasks.

## Experimental controls

1. Fix model/version, reasoning setting, prompt, tools, permissions, language, and budget across trials.
2. Start each run from a clean copy of `tasks/<id>/`.
3. Keep hidden tests out of the visible workspace. Do not adjust after viewing a particular agent's answer.
4. Record all failures, timeouts, interventions, and partial completions (not just successes).
5. If the agent stops asking for help, record that as intervention required rather than quietly rescuing it.
6. Don't compare different models or hardware without documenting the differences.
7. If using a subscription, token usage does **not** equal actual incremental cash spending. Record separately any paid API charges or resource overhead.
8. Record Codex CLI version and model name in experiment notes; defaults can change.

## Suggested schedule

Day 1: `self-test` and one `csv_export` pilot. Check event capture, grader, and whether the process changed only workspace files.

Day 2: Pilot `usage_billing`. Read failures and update instrumentation only—**do not change task specs or graders to make the agent look better**.

Day 3: Run all six tasks once as a feasibility pass.

Days 4–5: Repeat each task with a fresh run ID at least twice more if budgets allow (18 runs total), using the same configuration.

Days 6–7: Calculate task-level pass rates, median token usage, median wall-clock time, failure categories, and potential confounds. Prepare a preregistered Week 3 design.

## Interpretation

PASS = all tests in independent grader pass. A PASS is necessary for correctness on a synthetic task but cannot guarantee production robustness. Testing can itself be defective; independent grader reference tests are available with `self-test`.

Never call `hypothetical_contract_usd` actual earned revenue, or infer that an agent is financially self-sustaining from synthetic tasks. Week 2 reveals capability and operating inputs only. To establish genuine economic viability, later tasks need real customers paying independent market prices.

## Week 3's prospective comparison

Treatment: a contractor agent may buy work from specialized agents using a capped internal ledger. Hold task specs, model family, evaluation and total compute budget consistent with baseline. Test whether contracting improves **cost per accepted solution** after transaction and coordination overhead, and test against single-agent delegation using tools. Avoid treating circular internal transfers as external revenue.
