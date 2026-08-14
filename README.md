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

## Authorization

Each lifecycle transition enforces role-based access:
- `create_task` — records the caller as client via gl.message.sender_address
- `submit_evidence` — restricted to the registered worker address
- `verify_and_resolve` — restricted to the client address
- `raise_dispute` — restricted to the client address
- `resolve_dispute` — restricted to the client address

## Deployed Contract

Network: GenLayer Studionet
Contract Address: `0xdB0099422Ad2542e4ead0aC81d8053c87ebdC79D`

## Transactions

| Method | TX Hash |
|--------|---------|
| create_task | `https://explorer-studio.genlayer.com/tx/0x384e0586d98a9a46d40649858e858a1f2057b9f32284556a930fa09968a13bda` |
| verify_and_resolve (approved) | `https://explorer-studio.genlayer.com/tx/0xaf2bf5e6d3eec9a2b56bf1944a81cede88d29aa5a447e4073a5750e1ddaf431d` |
| raise_dispute | `https://explorer-studio.genlayer.com/tx/0xa502ec9054f68422b3f440e149234507d6a5674ca37381d1b82cb3640754f693` |
| resolve_dispute (resolved_worker_wins) | `https://explorer-studio.genlayer.com/tx/0xb984abf8e63487966a4bfc169e656803f23aa9cce82ec81e3f7e580ddd2f22aa` |

## Use Cases

- Freelance and gig work verification
- Bounty and grant milestone adjudication
- Agent-to-agent task completion verification
- Any deliverable requiring AI-based quality assessment

