from __future__ import annotations

from datetime import datetime, timezone

from .models import Conference, HistoricalDeadline


def _utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


CONFERENCES: tuple[Conference, ...] = (
    Conference(
        slug="cvpr",
        name="IEEE/CVF Conference on Computer Vision and Pattern Recognition",
        tier="A*",
        fields=("Computer Vision",),
        official_url="https://cvpr.thecvf.com/",
        deadline_urls=(
            "https://cvpr.thecvf.com/Conferences/2026/CallForPapers",
            "https://cvpr.thecvf.com/Conferences/2026/Dates",
            "https://cvpr.thecvf.com/",
        ),
        deadline_keywords=("paper submission deadline", "final paper submission", "submission deadline"),
        historical_deadlines=(
            HistoricalDeadline(2026, _utc("2025-11-13T23:59:00"), "Official call for papers"),
            HistoricalDeadline(2025, _utc("2024-11-14T23:59:00"), "Official call for papers"),
            HistoricalDeadline(2024, _utc("2023-11-17T23:59:00"), "Official call for papers"),
        ),
    ),
    Conference(
        slug="iccv",
        name="IEEE/CVF International Conference on Computer Vision",
        tier="A*",
        fields=("Computer Vision",),
        official_url="https://iccv.thecvf.com/",
        deadline_urls=(
            "https://iccv.thecvf.com/Conferences/2025/CallForPapers",
            "https://iccv.thecvf.com/Conferences/2025/Dates",
            "https://iccv.thecvf.com/",
        ),
        deadline_keywords=("paper submission deadline", "submission deadline"),
        historical_deadlines=(
            HistoricalDeadline(2025, _utc("2025-03-07T23:59:00"), "Official call for papers"),
            HistoricalDeadline(2023, _utc("2023-03-08T23:59:00"), "Official call for papers"),
            HistoricalDeadline(2021, _utc("2021-03-17T23:59:00"), "Official call for papers"),
        ),
    ),
    Conference(
        slug="eccv",
        name="European Conference on Computer Vision",
        tier="A",
        fields=("Computer Vision",),
        official_url="https://eccv.ecva.net/",
        deadline_urls=(
            "https://eccv.ecva.net/Conferences/2026/SubmissionPolicies",
            "https://eccv.ecva.net/Conferences/2026/Dates",
            "https://eccv.ecva.net/",
        ),
        deadline_keywords=("paper submission deadline", "submission deadline", "submission"),
        historical_deadlines=(
            HistoricalDeadline(2026, _utc("2026-03-06T12:59:00"), "Official important dates"),
            HistoricalDeadline(2024, _utc("2024-03-07T12:59:00"), "Official important dates"),
            HistoricalDeadline(2022, _utc("2022-03-07T23:59:00"), "Official important dates"),
        ),
    ),
    Conference(
        slug="sigcomm",
        name="ACM SIGCOMM",
        tier="A*",
        fields=("IoT", "Networking"),
        official_url="https://conferences.sigcomm.org/sigcomm/",
        deadline_urls=(
            "https://conferences.sigcomm.org/sigcomm/2026/cfp.html",
            "https://conferences.sigcomm.org/sigcomm/2026/",
            "https://conferences.sigcomm.org/sigcomm/",
        ),
        deadline_keywords=("paper submission deadline", "abstract registration", "submission deadline"),
        historical_deadlines=(
            HistoricalDeadline(2026, _utc("2026-01-31T23:59:00"), "Official CFP"),
            HistoricalDeadline(2025, _utc("2025-01-31T23:59:00"), "Official CFP"),
            HistoricalDeadline(2024, _utc("2024-02-02T23:59:00"), "Official CFP"),
        ),
    ),
    Conference(
        slug="sensys",
        name="ACM Conference on Embedded Networked Sensor Systems",
        tier="A",
        fields=("IoT", "Sensor Networks"),
        official_url="https://sensys.acm.org/",
        deadline_urls=(
            "https://sensys.acm.org/2026/",
            "https://sensys.acm.org/2026/cfp/",
            "https://sensys.acm.org/",
        ),
        deadline_keywords=("paper registration", "paper submission", "submission deadline"),
        historical_deadlines=(
            HistoricalDeadline(2025, _utc("2025-04-03T23:59:00"), "Official CFP"),
            HistoricalDeadline(2024, _utc("2024-04-04T23:59:00"), "Official CFP"),
            HistoricalDeadline(2023, _utc("2023-04-06T23:59:00"), "Official CFP"),
        ),
    ),
    Conference(
        slug="ipsn",
        name="ACM/IEEE International Conference on Information Processing in Sensor Networks",
        tier="A",
        fields=("IoT", "Sensor Networks"),
        official_url="https://ipsn.acm.org/",
        deadline_urls=(
            "https://ipsn.acm.org/2026/",
            "https://ipsn.acm.org/2026/call-for-papers/",
            "https://ipsn.acm.org/",
        ),
        deadline_keywords=("paper submission", "submission deadline", "abstract registration"),
        historical_deadlines=(
            HistoricalDeadline(2026, _utc("2025-10-15T23:59:00"), "Official CFP"),
            HistoricalDeadline(2025, _utc("2024-10-16T23:59:00"), "Official CFP"),
            HistoricalDeadline(2024, _utc("2023-10-17T23:59:00"), "Official CFP"),
        ),
    ),
    Conference(
        slug="icra",
        name="IEEE International Conference on Robotics and Automation",
        tier="A",
        fields=("Drone", "Robotics"),
        official_url="https://www.ieee-icra.org/",
        deadline_urls=(
            "https://2026.ieee-icra.org/",
            "https://2026.ieee-icra.org/call-for-papers/",
            "https://www.ieee-icra.org/",
        ),
        deadline_keywords=("paper submission deadline", "submission deadline", "full paper submission"),
        historical_deadlines=(
            HistoricalDeadline(2026, _utc("2025-09-15T23:59:00"), "Official CFP"),
            HistoricalDeadline(2025, _utc("2024-09-15T23:59:00"), "Official CFP"),
            HistoricalDeadline(2024, _utc("2023-09-15T23:59:00"), "Official CFP"),
        ),
    ),
    Conference(
        slug="iros",
        name="IEEE/RSJ International Conference on Intelligent Robots and Systems",
        tier="A",
        fields=("Drone", "Robotics"),
        official_url="https://www.ieee-iros.org/",
        deadline_urls=(
            "https://www.iros26.org/",
            "https://www.iros26.org/call-for-papers",
            "https://www.ieee-iros.org/",
        ),
        deadline_keywords=("paper submission deadline", "submission deadline"),
        historical_deadlines=(
            HistoricalDeadline(2026, _utc("2026-03-01T23:59:00"), "Official CFP"),
            HistoricalDeadline(2025, _utc("2025-03-01T23:59:00"), "Official CFP"),
            HistoricalDeadline(2024, _utc("2024-03-01T23:59:00"), "Official CFP"),
        ),
    ),
)


def get_conferences(fields: set[str] | None = None) -> tuple[Conference, ...]:
    if not fields:
        return CONFERENCES

    normalized_fields = {field.lower() for field in fields}
    return tuple(
        conference
        for conference in CONFERENCES
        if normalized_fields.intersection(field.lower() for field in conference.fields)
    )
