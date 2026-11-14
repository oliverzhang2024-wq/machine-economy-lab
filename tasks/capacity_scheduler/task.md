# Task 05 — Least-cost compute-job allocation

Implement `allocate(jobs, workers)`.

- Each job: `id`, `skill`, `units` (strictly positive integer), `priority` (integer).
- Each worker: `id`, `skills` (list of strings), `capacity` (nonnegative integer units), `unit_cost` (nonnegative integer cents).
- Process jobs in descending priority, breaking ties by lexicographically ascending job ID.
- For each job, choose the eligible worker with required skill and enough REMAINING capacity, minimizing unit_cost; break cost ties by lexicographically ascending worker ID.
- Assign all units of a job to ONE worker; do not split jobs.
- Return a dictionary mapping EACH job ID to its assigned worker ID or `None` when no worker qualifies.
- Do not mutate inputs. Raise `ValueError` for duplicate job/worker IDs or invalid units/capacities/costs.
- Use only standard library.
