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
    def create_task(self, worker: str, description: str) -> None:
        caller = str(gl.message.sender_address).lower()
        self.descriptions.append(description)
        self.evidence_urls.append("")
        self.statuses.append("open")
        self.results.append("")
        self.verdicts.append("")
        self.clients.append(caller)
        self.workers.append(worker.lower())
        self.task_count += u256(1)

    @gl.public.write
    def submit_evidence(self, task_id: u256, evidence_url: str) -> None:
        idx = int(task_id)
        caller = str(gl.message.sender_address).lower()
        assert self.statuses[idx] == "open", "Task must be open"
        assert caller == self.workers[idx], "Only the worker can submit evidence"
        self.evidence_urls[idx] = evidence_url
        self.statuses[idx] = "submitted"

    @gl.public.write
    def verify_and_resolve(self, task_id: u256) -> None:
        idx = int(task_id)
        caller = str(gl.message.sender_address).lower()
        assert self.statuses[idx] == "submitted", "Task must be submitted first"
        assert caller == self.clients[idx], "Only the client can trigger verification"

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
Respond ONLY with one word: approved or rejected
"""
            result = gl.nondet.exec_prompt(prompt)
            verdict = result.strip().lower()
            if "approved" in verdict:
                return "approved"
            return "rejected"

        raw = gl.eq_principle.prompt_comparative(
            fetch_and_evaluate,
            principle="Both validators must return the same single word: approved or rejected.",
        )

        verdict = raw.strip().lower()
        if "approved" in verdict:
            verdict = "approved"
        else:
            verdict = "rejected"

        self.verdicts[idx] = verdict
        self.results[idx] = verdict
        if verdict == "approved":
            self.statuses[idx] = "approved"
        else:
            self.statuses[idx] = "disputed"

    @gl.public.write
    def raise_dispute(self, task_id: u256, reason: str) -> None:
        idx = int(task_id)
        caller = str(gl.message.sender_address).lower()
        assert self.statuses[idx] == "approved", "Can only dispute approved tasks"
        assert caller == self.clients[idx], "Only the client can raise a dispute"
        self.results[idx] = "Disputed: " + reason
        self.verdicts[idx] = "disputed"
        self.statuses[idx] = "disputed"

    @gl.public.write
    def resolve_dispute(self, task_id: u256) -> None:
        idx = int(task_id)
        caller = str(gl.message.sender_address).lower()
        assert self.statuses[idx] == "disputed", "Task must be in disputed state"
        assert caller == self.clients[idx], "Only the client can resolve a dispute"

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

Evidence content fetched directly from the submission URL:
{page_content}

Based on the task description and the evidence above, who should win?
Respond ONLY with one of: worker_wins or client_wins
"""
            result = gl.nondet.exec_prompt(prompt)
            verdict = result.strip().lower()
            if "worker_wins" in verdict:
                return "worker_wins"
            return "client_wins"

        raw = gl.eq_principle.prompt_comparative(
            re_evaluate,
            principle="Both validators must return the same single verdict: worker_wins or client_wins.",
        )

        verdict = raw.strip().lower()
        if "worker_wins" in verdict:
            verdict = "worker_wins"
        else:
            verdict = "client_wins"

        self.verdicts[idx] = verdict
        self.results[idx] = verdict
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
