# Start the Week 2 experiment in GitHub Codespaces

This project is GitHub-first. **You do not need to download a ZIP or run Python on your Mac.**

1. Open the experiment's GitHub branch, click **Code → Codespaces → Create codespace on this branch**. Choose the default machine (typically 2 cores) for the pilot.
2. The Codespace devcontainer installs Python 3.12 and Codex CLI; its `postCreateCommand` runs `python3 lab.py self-test` to verify six grader/reference pairs.
3. In the Codespace terminal, run `codex login status`. If not authenticated, run `codex login --device-auth` and complete authorization in your browser. Device-code sign-in may first need to be enabled in your ChatGPT security settings. **Never paste tokens or passwords into GitHub files or this chat.**
4. Then run `python3 lab.py list`, followed by `python3 lab.py run csv_export --run-id pilot01 --timeout 600`. This **may consume model usage**; Codex is not automatically run just by opening the Codespace.
5. Review `runs/pilot01/workspace/solution.py`, `runs/pilot01/grader_output.txt`, and `runs/pilot01/result.json`.
6. `results.csv` is a compact tracked summary. If you want the latest results preserved in GitHub, check them for sensitive content and use VS Code Source Control to commit the updated CSV. Raw `runs/` is ignored by Git to avoid leaking tool traces and credentials.

If the Codex CLI is missing, run `npm install -g @openai/codex` in the Codespace terminal, then `codex --version`.

If login fails or your plan has exhausted its allowance, stop; do not bypass account restrictions. Use `python3 lab.py prepare csv_export --run-id manual01` for a manually driven, clearly distinguished run.

## Interpreting data

A task passes only if its independent grader accepts the solution. The grading suite was validated against reference solutions, but **we have not run Codex yet**. The test estimates engineering capability, **not** real customer demand, market value, or bank feasibility.

## Isolation

A Codespace is a development environment rather than an adversarial security sandbox for grader secrecy. The research protocol asks the agent not to inspect parent directories. For stronger blindness, future runs should place the agent in a separate isolated runtime that lacks graders and reference solutions entirely.

## Costs

Codespaces may have usage charges after included quotas; API-key Codex usage is billed separately. Record real cash spending separately from token counts or synthetic contract values.
