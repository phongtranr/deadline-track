from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, Iterable

from .conferences import CONFERENCES
from .crawler import extract_deadline, fetch_page
from .models import Conference, CrawlResult, DeadlineResult, DeadlineStatus
from .predictor import predict_next_deadline


Fetcher = Callable[[str], CrawlResult]


class DeadlineTracker:
    """Tracks official submission deadlines and predicts when live dates are unavailable."""

    def __init__(
        self,
        conferences: Iterable[Conference] = CONFERENCES,
        fetcher: Fetcher = fetch_page,
        now: Callable[[], datetime] | None = None,
    ) -> None:
        self._conferences = tuple(conferences)
        self._fetcher = fetcher
        self._now = now or (lambda: datetime.now(timezone.utc))

    def track(self, live: bool = True) -> tuple[DeadlineResult, ...]:
        return tuple(self.track_one(conference, live=live) for conference in self._conferences)

    def track_one(self, conference: Conference, live: bool = True) -> DeadlineResult:
        if live:
            live_result = self._crawl_live_deadline(conference)
            if live_result is not None:
                return live_result

        prediction = predict_next_deadline(conference, now=self._now())
        if prediction is not None:
            deadline, explanation = prediction
            return DeadlineResult(
                conference=conference,
                status=DeadlineStatus.PREDICTED,
                deadline=deadline,
                source_url=None,
                source_text=None,
                confidence=0.65,
                explanation=explanation,
            )

        return DeadlineResult(
            conference=conference,
            status=DeadlineStatus.UNKNOWN,
            deadline=None,
            source_url=None,
            source_text=None,
            confidence=0.0,
            explanation="No live deadline or historical data available.",
        )

    def _crawl_live_deadline(self, conference: Conference) -> DeadlineResult | None:
        for url in conference.deadline_urls:
            crawl = self._fetcher(url)
            if crawl.status != "ok":
                continue

            deadline = extract_deadline(crawl.text, conference.deadline_keywords)
            if deadline is None:
                continue

            return DeadlineResult(
                conference=conference,
                status=DeadlineStatus.LIVE,
                deadline=deadline,
                source_url=url,
                source_text=_source_excerpt(crawl.text, deadline),
                confidence=0.9,
                explanation="Extracted from the official conference website.",
            )
        return None


def _source_excerpt(text: str, deadline: datetime, width: int = 140) -> str | None:
    if not text:
        return None

    day = str(deadline.day)
    candidates = {
        f"{deadline.strftime('%B')} {day}, {deadline.year}",
        f"{deadline.strftime('%b')} {day}, {deadline.year}",
        deadline.strftime("%Y-%m-%d"),
        deadline.strftime("%Y/%m/%d"),
    }
    lowered = text.lower()
    for candidate in candidates:
        index = lowered.find(candidate.lower())
        if index != -1:
            start = max(0, index - width)
            end = min(len(text), index + len(candidate) + width)
            return text[start:end].strip()
    return None
