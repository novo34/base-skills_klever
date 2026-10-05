from __future__ import annotations

from staging.readiness import StagingReadinessEvidence


class StagingEvidenceStore:
    def __init__(self):
        self._items: dict[str, StagingReadinessEvidence] = {}
        self._task_index: dict[str, list[str]] = {}

    def append(self, evidence: StagingReadinessEvidence) -> StagingReadinessEvidence:
        if evidence.evidence_id in self._items:
            raise ValueError("staging_evidence_already_exists")
        self._items[evidence.evidence_id] = evidence
        self._task_index.setdefault(evidence.task_id, []).append(evidence.evidence_id)
        return evidence

    def get(self, evidence_id: str) -> StagingReadinessEvidence:
        if evidence_id not in self._items:
            raise KeyError("staging_evidence_not_found")
        return self._items[evidence_id]

    def latest_for_task(self, task_id: str) -> StagingReadinessEvidence | None:
        ids = self._task_index.get(task_id, [])
        if not ids:
            return None
        return self._items[ids[-1]]

    def replace(self, evidence_id: str, evidence: StagingReadinessEvidence) -> None:
        raise PermissionError("staging_evidence_is_immutable")

    def delete(self, evidence_id: str) -> None:
        raise PermissionError("staging_evidence_is_immutable")
