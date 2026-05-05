from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable


class DeadlineStatus(str, Enum):
    LIVE = "live"
    PREDICTED = "predicted"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class HistoricalDeadline:
    year: int
    deadline: datetime
    source: str


@dataclass(frozen=True)
class Conference:
    slug: str
    name: str
    fields: tuple[str, ...]
    tier: str
    official_url: str
    deadline_urls: tuple[str, ...]
    deadline_keywords: tuple[str, ...]
    historical_deadlines: tuple[HistoricalDeadline, ...]
    note: str = ""

    def ordered_history(self) -> tuple[HistoricalDeadline, ...]:
        return tuple(sorted(self.historical_deadlines, key=lambda item: item.year))


@dataclass(frozen=True)
class CrawlResult:
    url: str
    status: str
    text: str
    last_modified: datetime | None = None
    error: str | None = None


@dataclass(frozen=True)
class DeadlineResult:
    conference: Conference
    status: DeadlineStatus
    deadline: datetime | None
    source_url: str | None
    source_text: str | None
    confidence: float
    explanation: str

    def deadline_iso(self) -> str | None:
        if self.deadline is None:
            return None
        return self.deadline.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def tracks_for(results: Iterable[DeadlineResult]) -> tuple[str, ...]:
    return tuple(sorted({field for result in results for field in result.conference.fields}))
