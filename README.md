FreelanceTaskValidator — GenLayer Intelligent Contract

A reusable Intelligent Contract primitive for verifying freelance task completion using AI consensus.

## What It Does

FreelanceTaskValidator enables trustless verification of digital work deliverables. Instead of relying on a single party to evaluate whether a task was completed, multiple AI validators independently fetch the evidence URL, read its contents, and reach consensus on whether the work satisfies the task description.

## How GenLayer Consensus Is Used

The `verify_and_resolve` function uses `gl.eq_principle.prompt_comparative` — each validator independently fetches the evidence URL via `gl.nondet.web.get`, reads the content, and prompts an LLM to evaluate whether the deliverable satisfies the task description. Validators must reach the same verdict (approved/rejected) for the transaction to finalize.

The `resolve_dispute` function triggers a second round of AI consensus with the dispute reason included, allowing for a fair re-evaluation.

## Lifecycle

create_task → submit_evidence → verify_and_resolve → (raise_dispute → resolve_dispute)

- `open` — task created, waiting for submission
- `submitted` — evidence URL provided by worker
- `approved` — AI validators confirmed task completion
- `disputed` — client challenged the result or evidence was rejected
- `resolved_worker_wins` — arbitration confirmed worker completed the task
- `resolved_client_wins` — arbitration sided with client's dispute

## Deployed Contract

Network: GenLayer Studionet
Contract Address: `0x186182ceaD0eB4921A67feba42952a8076fFed42`

## Transactions

| Method | TX Hash |
|--------|---------|
| create_task | `https://explorer-studio.genlayer.com/tx/0x7f917d950211b41e48aeaca21dae8e5e28f4e1c9d7bfc28d9d45012a59d8f711` |
| verify_and_resolve (approved) | `https://explorer-studio.genlayer.com/tx/0xaa3d784bd1312ca3abef2d8f13f4323db88fb5f6f313586fde44e831071b13ad` |
| raise_dispute | `https://explorer-studio.genlayer.com/tx/0x3d694882eec46090f152b579e36c7c134b5db9b3809d95a36b9b5c47578f7bd0` |
| resolve_dispute (resolved_worker_wins) | `https://explorer-studio.genlayer.com/tx/0xa0b343309b477450ebe2725526f4775d7c0594a0766f85fb2f55a30026c600ec` |

## Use Cases

- Freelance and gig work verification
- Bounty and grant milestone adjudication
- Agent-to-agent task completion verification
- Any deliverable requiring AI-based quality assessment

