from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import sys

from .conferences import get_conferences
from .models import DeadlineResult
from .tracker import DeadlineTracker


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="deadline-track",
        description=(
            "Track live or predicted submission deadlines for A*/A conferences "
            "in Computer Vision, IoT, and Drone/Robotics."
        ),
    )
    parser.add_argument(
        "--field",
        action="append",
        choices=("Computer Vision", "IoT", "Drone", "Robotics", "Networking", "Sensor Networks"),
        help="Limit results to a field. Can be passed more than once.",
    )
    parser.add_argument(
        "--offline",
        "--no-live",
        action="store_true",
        help="Skip website crawling and show historical predictions only.",
    )
    parser.add_argument(
        "--format",
        choices=("table", "json"),
        default="table",
        help="Choose table or machine-readable JSON output.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of conferences returned.",
    )
    args = parser.parse_args(argv)

    conferences = get_conferences(set(args.field or ()))
    tracker = DeadlineTracker(conferences)
    results = tracker.track(live=not args.offline)

    if args.limit is not None:
        results = results[: args.limit]

    if args.format == "json":
        print(json.dumps([_result_to_dict(result) for result in results], indent=2))
    else:
        _print_table(results)
    return 0


def _result_to_dict(result: DeadlineResult) -> dict[str, object]:
    conference = result.conference
    return {
        "slug": conference.slug,
        "name": conference.name,
        "tier": conference.tier,
        "fields": conference.fields,
        "status": result.status.value,
        "deadline_utc": result.deadline_iso(),
        "source_url": result.source_url,
        "confidence": result.confidence,
        "explanation": result.explanation,
    }


def _print_table(results: tuple[DeadlineResult, ...]) -> None:
    now = datetime.now(timezone.utc)
    rows = []
    for result in results:
        deadline = result.deadline_iso() or "unknown"
        days = ""
        if result.deadline is not None:
            days = str((result.deadline.astimezone(timezone.utc) - now).days)
        rows.append(
            (
                result.conference.slug.upper(),
                "/".join(result.conference.fields),
                result.conference.tier,
                result.status.value,
                deadline,
                days,
                result.source_url or "-",
            )
        )

    headers = ("Conf", "Fields", "Tier", "Status", "Deadline UTC", "Days", "Source")
    widths = [len(header) for header in headers]
    for row in rows:
        widths = [max(width, len(value)) for width, value in zip(widths, row)]

    def fmt(row: tuple[str, ...]) -> str:
        return "  ".join(value.ljust(width) for value, width in zip(row, widths))

    print(fmt(headers))
    print(fmt(tuple("-" * width for width in widths)))
    for row in rows:
        print(fmt(row))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
