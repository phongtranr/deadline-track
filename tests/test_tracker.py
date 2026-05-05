from __future__ import annotations

from datetime import datetime, timezone

from deadline_track.models import Conference, CrawlResult, DeadlineStatus, HistoricalDeadline
from deadline_track.tracker import DeadlineTracker


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


def test_tracker_returns_live_deadline_when_official_page_has_submission_date() -> None:
    conference = Conference(
        slug="demo",
        name="DemoConf",
        tier="A",
        fields=("Computer Vision",),
        official_url="https://example.test",
        deadline_urls=("https://example.test/cfp",),
        deadline_keywords=("paper submission deadline",),
        historical_deadlines=(HistoricalDeadline(2025, _dt("2025-03-07T23:59:00"), "CFP"),),
    )

    def fetcher(url: str) -> CrawlResult:
        return CrawlResult(
            url=url,
            status="ok",
            text="Important dates: paper submission deadline is March 9, 2026 AoE.",
        )

    tracker = DeadlineTracker((conference,), fetcher=fetcher, now=lambda: _dt("2025-01-01T00:00:00"))

    result = tracker.track()[0]

    assert result.status == DeadlineStatus.LIVE
    assert result.deadline is not None
    assert result.deadline.year == 2026
    assert result.source_url == "https://example.test/cfp"


def test_tracker_falls_back_to_prediction_when_live_crawl_fails() -> None:
    conference = Conference(
        slug="demo",
        name="DemoConf",
        tier="A",
        fields=("IoT",),
        official_url="https://example.test",
        deadline_urls=("https://example.test/cfp",),
        deadline_keywords=("paper submission deadline",),
        historical_deadlines=(HistoricalDeadline(2025, _dt("2025-04-03T23:59:00"), "CFP"),),
    )

    tracker = DeadlineTracker(
        (conference,),
        fetcher=lambda url: CrawlResult(url=url, status="http_404", text=""),
        now=lambda: _dt("2025-05-01T00:00:00"),
    )

    result = tracker.track()[0]

    assert result.status == DeadlineStatus.PREDICTED
    assert result.deadline is not None
    assert result.deadline.year == 2026
