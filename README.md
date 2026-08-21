# FreelanceTaskValidator — GenLayer Intelligent Contract

A reusable Intelligent Contract primitive for verifying freelance task completion using AI consensus.

## What It Does

FreelanceTaskValidator enables trustless verification of digital work deliverables. Instead of relying on a single party to evaluate whether a task was completed, multiple AI validators independently fetch the evidence URL, read its contents, and reach consensus on whether the work satisfies the task description.

## How GenLayer Consensus Is Used

In `verify_and_resolve`, each validator independently fetches the evidence URL via `gl.nondet.web.get` and returns a single canonical verdict: `approved`, `rejected`, or `fetch_failed`. No free-form reasoning is stored at this stage, eliminating any risk of validators agreeing on verdict while disagreeing on reasoning.

In `resolve_dispute`, validators independently reacquire the evidence directly from the submission URL and determine `worker_wins`, `client_wins`, or `fetch_failed`. The final verdict drives the terminal state to `resolved_worker_wins` or `resolved_client_wins`.

Both rounds use `gl.eq_principle.prompt_comparative` to reach consensus.

## What's New in This Version

Two improvements were added based on steward feedback:

### Explicit Fetch/Decoding Failure Handling
If validators cannot fetch or decode the evidence URL (network error, unreachable host, empty page), the contract does not crash and does not incorrectly reject the task. Instead, task state is left unchanged (e.g. remains `submitted` or `disputed`) so the client can retry once the URL is reachable again. This follows the same pattern used in accepted primitives like Penumbra's SemanticDeadman, which distinguishes fetch failures from genuine negative outcomes.

### Structured Getters for Integrators
Instead of parsing a single concatenated string, integrators can now call individual view methods:
- `get_status(task_id)`
- `get_verdict(task_id)`
- `get_result(task_id)`
- `get_client(task_id)`
- `get_worker(task_id)`
- `get_description(task_id)`
- `get_evidence_url(task_id)`

The original `get_task(task_id)` remains available for backward compatibility.

## Lifecycle

create_task → submit_evidence → verify_and_resolve → (raise_dispute → resolve_dispute)

- `open` — task created, waiting for submission
- `submitted` — evidence URL provided by worker (also the state a task returns to if a fetch fails during verification)
- `approved` — AI validators confirmed task completion
- `disputed` — client challenged the result, evidence was rejected, or a fetch failed during arbitration (task stays disputed until retried)
- `resolved_worker_wins` — arbitration confirmed worker completed the task
- `resolved_client_wins` — arbitration sided with client's dispute

## Authorization

Each lifecycle transition enforces role-based access:
- `create_task` — records the caller as client via gl.message.sender_address
- `submit_evidence` — restricted to the registered worker address
- `verify_and_resolve` — restricted to the client address
- `raise_dispute` — restricted to the client address
- `resolve_dispute` — restricted to the client address

## Deployed Contract

Network: GenLayer Studionet
Contract Address: `0xAae9E1398dB3E08fCB1ec7e9D8ac4025fb91375a`

## Transactions

| Method | TX Hash |
|--------|---------|
| create_task | `https://explorer-studio.genlayer.com/tx/0xd97d5ec3d2f3ea7fbdb7694337edef2dc2d317fa9549658bccf3a3d4883057ee` |
| submit_evidence | `https://explorer-studio.genlayer.com/tx/0x0dcb2a82357d59ee18a8b009835d3776277b21f7ba1b61502019a76cb8070b87` |
| verify_and_resolve (approved) | `https://explorer-studio.genlayer.com/tx/0xf8d857f90895a13966d21b3c7d1b8181aeb9d71691d934835ebfdfa62553ba6d` |
| create_task (fetch failure test) | `https://explorer-studio.genlayer.com/tx/0xe4a1b12f2e2dc0bce7332087c758f45704b8fd87e4ab95255e347b0c3163dfb6` |
| submit_evidence (broken URL) | `https://explorer-studio.genlayer.com/tx/0xbbf7159f70e59deaf25c77a4f3b728bc0636a4e072eed3dbabd7b589a85849df` |
| verify_and_resolve (fetch_failed, state unchanged) | `https://explorer-studio.genlayer.com/tx/0x23b22cb3d5a25e2f854b42e349fe6bf7aebbb6088f4325f6d5a787844ed65b82` |
| raise_dispute | `https://explorer-studio.genlayer.com/tx/0xd6841cc6c0476dc8114ffa752f4df0649ac522024f3b0f0199606dcd92e57a5a` |
| resolve_dispute (resolved_worker_wins) | `https://explorer-studio.genlayer.com/tx/0xe129b935d3e016b49f6bdb37feee4343f62ee148a98fc0d0315479758d2123ef` |

## Use Cases

- Freelance and gig work verification
- Bounty and grant milestone adjudication
- Agent-to-agent task completion verification
- Any deliverable requiring AI-based quality assessment
