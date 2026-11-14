# Machine Economy Lab — Week 2

**Objective:** measure the reliability, resource consumption, and time required for a *single* AI coding agent to complete small, reproducible software tasks. In Week 3, we can compare the same task set with multi-agent contracting, with baseline conditions held constant.

This is an educational research experiment, not a production payment system. No deposits, tokens, loans, customers, revenue, or actual transfers are created. **The six tasks are researcher-issued benchmarks, not paid customer jobs.** See `ECONOMY_EXPLAINED.md`.

## What is in this kit?

- `tasks/`: six tasks, each with a written specification, a stub in `solution.py`, and a public example check.
- `graders/`: independent tests run **after** the agent submits its implementation.
- `references/`: correct solutions used only to confirm that graders are valid (never show them to a tested agent).
- `lab.py`: CLI that prepares workspaces, runs one Codex agent, captures usage, grades the result, and writes `results.csv`.
- `EXPERIMENT_PROTOCOL.md`: how to run a defensible pilot.
- `hypotheses.md`: the initial research hypotheses and disconfirmation criteria.

## Prerequisites

- macOS/Linux/Windows with Python **3.10+**.
- For automated agent runs, install and sign in to the **Codex CLI**. Its current official installation instructions are at https://learn.chatgpt.com/docs/codex/cli. A ChatGPT sign-in may support Codex usage under your account plan; API-key authentication is separately billed. Check the terms of your own account before running experiments.
- The Python experiment requires **no pip installations** and no model API key in the code.

## Quick start (GitHub Codespaces recommended)

Open `CODESPACES_RUNBOOK.md` for a cloud-only workflow and `ECONOMY_EXPLAINED.md` for who creates work, what is paid, and why Week 2 has no real customer revenue.

## Alternative: local Mac terminal

1. Extract `machine-economy-lab-week2.zip` to a folder you control.
2. Open Terminal and change into that folder (`cd /path/to/machine_economy_lab`).
3. Verify the kit:

```bash
python3 lab.py self-test
python3 lab.py list
```

4. Confirm your Codex CLI is installed and authenticated:

```bash
codex --version
codex login
```

5. Run the **first single-agent experiment**:

```bash
python3 lab.py run csv_export --run-id pilot01
```

The script creates `runs/pilot01/workspace`, passes the task to Codex, captures JSONL events, then runs independent tests. It will print PASS/FAIL. To review its work:

```bash
cat runs/pilot01/workspace/solution.py
cat runs/pilot01/grader_output.txt
cat results.csv
```

6. After reviewing the pilot, try the next task with a new run ID:

```bash
python3 lab.py run usage_billing --run-id pilot02
```

To fix the model for all runs (if a specific model is supported by your installed Codex CLI), add `--model MODEL_NAME`. Use the same model and settings for baseline and comparative runs. Otherwise record your actual model setting manually; the script marks the configured default as unverified.

### If you want to run Codex interactively instead

```bash
python3 lab.py prepare csv_export --run-id manual01
cd runs/manual01/workspace
codex
```

In Codex, ask it to implement `task.md` in `solution.py` and run `python3 example_check.py`. Afterwards, `cd` back to the kit root and run:

```bash
python3 lab.py evaluate manual01
```

Manual mode does not automatically measure tokens or elapsed time; record those separately. For reproducible work, the `run` command is preferred.

## What is measured?

- Completion against independent unit tests, not just the agent's own confidence.
- Total wall-clock time for the Codex process.
- Token usage reported by `turn.completed` JSONL events (when available).
- Full agent trace and grader outcome for review.

**What is deliberately NOT inferred:** cash costs from a ChatGPT subscription, hypothetical sale price as real revenue, a profitable economic agent, a financing gap, or human task value. `actual_cash_cost_usd`, `estimated_api_cost_usd`, and `net_income_usd` are left blank, rather than invented.

`hypothetical_contract_usd` is a placeholder task reward to be used only in a clearly labeled *simulation* later. It is not a real customer price.

## Research hygiene

- Keep the grader and reference solutions outside any agent workspace; do not ask the agent to inspect them. This is **research separation, not a hard security boundary**. A container/VM is required for true isolation from host files, credentials, or network access.
- Do not run agents with production credentials, unrestricted shell permissions, or in important repositories.
- Do not use `--dangerously-bypass-approvals-and-sandbox`.
- Don't change grading rules between baseline and comparison runs.
- Keep task scope and prompt unchanged across repeated runs.
- A single PASS/FAIL is only a pilot; run multiple independent trials before attempting to draw conclusions.

## Next research decision

If a single agent completes the tasks well and economically, design Week 3's multi-agent comparison. If it fails, understand whether the problem is missing instructions, unreliable software production, or evaluation design—**not** automatically a need for financial infrastructure.
