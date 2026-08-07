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
- `disputed` — client challenged the result
- `resolved` — final AI arbitration completed

## Deployed Contract

Network: GenLayer Studionet
Contract Address: `0x659037871d5BAD38514275c6030D923765f71b5f`

## Transactions

| Method | TX Hash |
|--------|---------|
| create_task | `https://explorer-studio.genlayer.com/tx/0x567a896e5fdb64066e6771eea540a345ed870afef149337405597cd08181441e` |
| verify_and_resolve (approved) | `https://explorer-studio.genlayer.com/tx/0xf92ededdd77a3d21329859dc5777997b42decddf3a7b4cb72c8289d350389f48` |
| raise_dispute | `https://explorer-studio.genlayer.com/tx/0xb37310ac8557e80129e920619e47e14ca60a445d8a3c9dcc8d80d280595c7a2b` |
| resolve_dispute (resolved_worker_wins) | `https://explorer-studio.genlayer.com/tx/0x293a1d985091f7f3c9c91ce75d98acaf425ab641f316be18283e0449e25a69e9` |

## Use Cases

- Freelance and gig work verification
- Bounty and grant milestone adjudication
- Agent-to-agent task completion verification
- Any deliverable requiring AI-based quality assessment

