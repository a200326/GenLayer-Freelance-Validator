# FreelanceTaskValidator — GenLayer Intelligent Contract

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
- `disputed` — client challenged the result
- `resolved` — final AI arbitration completed

## Deployed Contract

Network: GenLayer Studionet
Contract Address: `0x323220f33cc5A0Cd83242eB4f571A27D7012E2d2`

## Transactions

| Method | TX Hash |
|--------|---------|
| create_task (task 0) | `[TX_HASH](https://explorer-studio.genlayer.com/tx/0x622d6ba4fdab36d96e4eef6e0c9333907b965fa84ba40932db949361c78bfbd8)` |
| verify_and_resolve (task 1 - approved) | `[TX_HASH](https://explorer-studio.genlayer.com/tx/0xdbb4befb7b294863e8e26427f5dae688224c1558cda1f3b3c3a9be6c27cb2304)` |
| resolve_dispute (task 2 - resolved) | `[TX_HASH](https://explorer-studio.genlayer.com/tx/0xa2df0a65e9e7ed65246d50aef3d7b23097daa1df88507df147abb43c29d7a2df)` |

## Use Cases

- Freelance and gig work verification
- Bounty and grant milestone adjudication
- Agent-to-agent task completion verification
- Any deliverable requiring AI-based quality assessment

