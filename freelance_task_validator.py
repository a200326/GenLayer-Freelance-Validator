# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json

FETCH_FAILED = "fetch_failed"

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
            try:
                resp = gl.nondet.web.get(evidence_url)
                page_content = resp.body.decode("utf-8")[:3000]
            except Exception:
                return FETCH_FAILED

            if not page_content.strip():
                return FETCH_FAILED

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
            principle="Both validators must return the same single word: approved, rejected, or fetch_failed.",
        )

        verdict = raw.strip().lower()

        if verdict == FETCH_FAILED:
            self.results[idx] = "Evidence could not be fetched or was empty. Task remains submitted; please retry verify_and_resolve once the URL is reachable."
            return

        if verdict == "approved":
            self.verdicts[idx] = "approved"
            self.results[idx] = "approved"
            self.statuses[idx] = "approved"
        else:
            self.verdicts[idx] = "rejected"
            self.results[idx] = "rejected"
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
            try:
                resp = gl.nondet.web.get(evidence_url)
                page_content = resp.body.decode("utf-8")[:3000]
            except Exception:
                return FETCH_FAILED

            if not page_content.strip():
                return FETCH_FAILED

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
            principle="Both validators must return the same single verdict: worker_wins, client_wins, or fetch_failed.",
        )

        verdict = raw.strip().lower()

        if verdict == FETCH_FAILED:
            self.results[idx] = "Evidence could not be fetched during arbitration. Task remains disputed; please retry resolve_dispute once the URL is reachable."
            return

        self.verdicts[idx] = verdict
        self.results[idx] = verdict
        if verdict == "worker_wins":
            self.statuses[idx] = "resolved_worker_wins"
        else:
            self.statuses[idx] = "resolved_client_wins"

    # ---- Structured getters for integrators ----

    @gl.public.view
    def get_status(self, task_id: u256) -> str:
        return self.statuses[int(task_id)]

    @gl.public.view
    def get_verdict(self, task_id: u256) -> str:
        return self.verdicts[int(task_id)]

    @gl.public.view
    def get_result(self, task_id: u256) -> str:
        return self.results[int(task_id)]

    @gl.public.view
    def get_client(self, task_id: u256) -> str:
        return self.clients[int(task_id)]

    @gl.public.view
    def get_worker(self, task_id: u256) -> str:
        return self.workers[int(task_id)]

    @gl.public.view
    def get_description(self, task_id: u256) -> str:
        return self.descriptions[int(task_id)]

    @gl.public.view
    def get_evidence_url(self, task_id: u256) -> str:
        return self.evidence_urls[int(task_id)]

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
