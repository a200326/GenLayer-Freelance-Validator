# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json

class FreelanceTaskValidator(gl.Contract):
    descriptions: DynArray[str]
    evidence_urls: DynArray[str]
    statuses: DynArray[str]
    results: DynArray[str]
    verdicts: DynArray[str]
    clients: DynArray[str]
    workers: DynArray[str]
    task_count: u256

    def __init__(self):
        self.task_count = u256(0)

    @gl.public.write
    def create_task(self, client: gl.Address, worker: gl.Address, description: str) -> None:
        self.descriptions.append(description)
        self.evidence_urls.append("")
        self.statuses.append("open")
        self.results.append("")
        self.verdicts.append("")
        self.clients.append(str(client))
        self.workers.append(str(worker))
        self.task_count += u256(1)

    @gl.public.write
    def submit_evidence(self, task_id: u256, evidence_url: str) -> None:
        idx = int(task_id)
        assert self.statuses[idx] == "open", "Task must be open"
        self.evidence_urls[idx] = evidence_url
        self.statuses[idx] = "submitted"

    @gl.public.write
    def verify_and_resolve(self, task_id: u256) -> None:
        idx = int(task_id)
        assert self.statuses[idx] == "submitted", "Task must be submitted first"

        description = self.descriptions[idx]
        evidence_url = self.evidence_urls[idx]

        def fetch_and_evaluate() -> str:
            resp = gl.nondet.web.get(evidence_url)
            page_content = resp.body.decode("utf-8")[:3000]
            prompt = f"""
You are a neutral evaluator for a freelance task.

Task description: {description}

Evidence content:
{page_content}

Has the task been completed satisfactorily?
Respond ONLY with a JSON object (no markdown, no backticks):
{{"verdict": "approved", "reasoning": "one sentence"}}
or
{{"verdict": "rejected", "reasoning": "one sentence"}}
"""
            result = gl.nondet.exec_prompt(prompt)
            return result.strip()

        raw = gl.eq_principle.prompt_comparative(
            fetch_and_evaluate,
            principle="Both validators must reach the same verdict (approved or rejected).",
        )

        try:
            parsed = json.loads(raw)
            verdict = parsed.get("verdict", "rejected")
            reasoning = parsed.get("reasoning", "")
        except Exception:
            verdict = "rejected"
            reasoning = "Could not parse evaluator response"

        self.results[idx] = reasoning
        self.verdicts[idx] = verdict
        if verdict == "approved":
            self.statuses[idx] = "approved"
        else:
            self.statuses[idx] = "disputed"

    @gl.public.write
    def raise_dispute(self, task_id: u256, reason: str) -> None:
        idx = int(task_id)
        assert self.statuses[idx] == "approved", "Can only dispute approved tasks"
        self.results[idx] = "Disputed: " + reason
        self.verdicts[idx] = "disputed"
        self.statuses[idx] = "disputed"

    @gl.public.write
    def resolve_dispute(self, task_id: u256) -> None:
        idx = int(task_id)
        assert self.statuses[idx] == "disputed", "Task must be in disputed state"

        description = self.descriptions[idx]
        evidence_url = self.evidence_urls[idx]
        dispute_reason = self.results[idx]

        def re_evaluate() -> str:
            resp = gl.nondet.web.get(evidence_url)
            page_content = resp.body.decode("utf-8")[:3000]
            prompt = f"""
You are a senior arbitrator reviewing a disputed freelance task.

Task description: {description}
Dispute reason: {dispute_reason}

Evidence content:
{page_content}

Who should win this dispute?
Respond ONLY with a JSON object (no markdown, no backticks):
{{"verdict": "worker_wins", "reasoning": "one sentence"}}
or
{{"verdict": "client_wins", "reasoning": "one sentence"}}
"""
            result = gl.nondet.exec_prompt(prompt)
            return result.strip()

        raw = gl.eq_principle.prompt_comparative(
            re_evaluate,
            principle="Both validators must agree on the final arbitration verdict.",
        )

        try:
            parsed = json.loads(raw)
            verdict = parsed.get("verdict", "client_wins")
            reasoning = parsed.get("reasoning", "")
        except Exception:
            verdict = "client_wins"
            reasoning = "Could not parse arbitration response"

        self.verdicts[idx] = verdict
        self.results[idx] = reasoning
        if verdict == "worker_wins":
            self.statuses[idx] = "resolved_worker_wins"
        else:
            self.statuses[idx] = "resolved_client_wins"

    @gl.public.view
    def get_task(self, task_id: u256) -> str:
        idx = int(task_id)
        return (
            "status: " + self.statuses[idx] +
            " | verdict: " + self.verdicts[idx] +
            " | client: " + self.clients[idx] +
            " | worker: " + self.workers[idx] +
            " | result: " + self.results[idx]
        )

    @gl.public.view
    def get_task_count(self) -> u256:
        return self.task_count
