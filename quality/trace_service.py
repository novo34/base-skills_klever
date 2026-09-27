from __future__ import annotations

from quality.ingestion import QualityTraceIngestor
from quality.service import QualityService


class TraceDrivenQualityService:
    def __init__(
        self,
        *,
        ingestor: QualityTraceIngestor | None = None,
        quality: QualityService | None = None,
    ):
        self.ingestor = ingestor or QualityTraceIngestor()
        self.quality = quality or QualityService()

    def summarize_trace_dicts(self, records: list[dict]) -> dict:
        items = self.ingestor.from_trace_dicts(records)
        return self.quality.summarize(items)
