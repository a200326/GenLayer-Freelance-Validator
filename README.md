FreelanceTaskValidator — GenLayer Intelligent Contract

A reusable Intelligent Contract primitive for verifying freelance task completion using AI consensus.

## What It Does

FreelanceTaskValidator enables trustless verification of digital work deliverables. Instead of relying on a single party to evaluate whether a task was completed, multiple AI validators independently fetch the evidence URL, read its contents, and reach consensus on whether the work satisfies the task description.

## How GenLayer Consensus Is Used

In `verify_and_resolve`, each validator independently fetches the evidence URL via `gl.nondet.web.get` and returns a single canonical verdict: `approved` or `rejected`. No free-form reasoning is stored, eliminating any risk of validators agreeing on verdict while disagreeing on reasoning.

In `resolve_dispute`, validators independently reacquire the evidence directly from the submission URL and determine `worker_wins` or `client_wins`. The final verdict drives the terminal state to `resolved_worker_wins` or `resolved_client_wins`.

Both rounds use `gl.eq_principle.prompt_comparative` to reach consensus.

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
Contract Address: `0x7Ed4C98Ae328c192dAC5fa72F76EAF87e5cA60Be`

## Transactions

| Method | TX Hash |
|--------|---------|
| create_task | `https://explorer-studio.genlayer.com/tx/0x3401875f3e299cbbfbdea1e084205230603fdda1a2be7fcf759dc5b66136690e` |
| verify_and_resolve (approved) | `https://explorer-studio.genlayer.com/tx/0x88058c974f89711b2e5bfe2181e92059a9ef997a56dd4aef05e670a5dd5cc65f` |
| raise_dispute | `https://explorer-studio.genlayer.com/tx/0xa6a1c82155596fce834991f813d3e5bea65942ee9acbd7b99b6f2444b056dd94` |
| resolve_dispute (resolved_worker_wins) | `https://explorer-studio.genlayer.com/tx/0x9b9bbfc9cf489f55cd99d6efea23aa847e1a6ac5531ede54139f27becaa77056` |

## Use Cases

- Freelance and gig work verification
- Bounty and grant milestone adjudication
- Agent-to-agent task completion verification
- Any deliverable requiring AI-based quality assessment

