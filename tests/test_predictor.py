from __future__ import annotations

from datetime import datetime, timezone

from deadline_track.models import Conference, HistoricalDeadline
from deadline_track.predictor import predict_next_deadline


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


def test_predicts_next_annual_deadline_from_latest_year() -> None:
    conference = Conference(
        slug="demo",
        name="DemoConf",
        tier="A",
        fields=("IoT",),
        official_url="https://example.test",
        deadline_urls=(),
        deadline_keywords=("submission deadline",),
        historical_deadlines=(
            HistoricalDeadline(2024, _dt("2024-04-04T23:59:00"), "CFP"),
            HistoricalDeadline(2025, _dt("2025-04-03T23:59:00"), "CFP"),
        ),
    )

    predicted = predict_next_deadline(conference, now=_dt("2025-05-01T00:00:00"))
    assert predicted is not None
    deadline, explanation = predicted
    assert deadline is not None
    assert deadline.year == 2026
    assert deadline.month == 4
    assert deadline.day == 3
    assert "historical" in explanation


def test_predicts_next_biennial_deadline() -> None:
    conference = Conference(
        slug="demo",
        name="DemoConf",
        tier="A*",
        fields=("Computer Vision",),
        official_url="https://example.test",
        deadline_urls=(),
        deadline_keywords=("submission deadline",),
        historical_deadlines=(
            HistoricalDeadline(2021, _dt("2021-03-17T23:59:00"), "CFP"),
            HistoricalDeadline(2023, _dt("2023-03-08T23:59:00"), "CFP"),
            HistoricalDeadline(2025, _dt("2025-03-07T23:59:00"), "CFP"),
        ),
    )

    predicted = predict_next_deadline(conference, now=_dt("2025-04-01T00:00:00"))
    assert predicted is not None
    deadline, _ = predicted
    assert deadline is not None
    assert deadline.year == 2027
    assert deadline.month == 3
    assert deadline.day == 7
