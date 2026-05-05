from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from deadline_track.conferences import CONFERENCES
from deadline_track.tracker import DeadlineTracker


def main() -> int:
    parser = argparse.ArgumentParser(description="Build static JSON data for the GitHub Pages site.")
    parser.add_argument(
        "--output",
        default="docs/data/deadlines.json",
        help="Path to write generated deadline data.",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Skip website crawling and publish prediction-only data.",
    )
    args = parser.parse_args()

    tracker = DeadlineTracker(CONFERENCES)
    results = tracker.track(live=not args.offline)
    generated_at = datetime.now(timezone.utc)

    payload = {
        "generated_at": generated_at.isoformat().replace("+00:00", "Z"),
        "live_crawl": not args.offline,
        "conferences": [_result_to_dict(result, generated_at) for result in results],
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(results)} conference deadlines to {output}")
    return 0


def _result_to_dict(result, generated_at: datetime) -> dict[str, object]:
    deadline = result.deadline
    days_until = None
    if deadline is not None:
        days_until = (deadline.astimezone(timezone.utc) - generated_at).days

    conference = result.conference
    return {
        "slug": conference.slug,
        "name": conference.name,
        "tier": conference.tier,
        "fields": list(conference.fields),
        "official_url": conference.official_url,
        "deadline_urls": list(conference.deadline_urls),
        "status": result.status.value,
        "deadline_utc": result.deadline_iso(),
        "days_until": days_until,
        "source_url": result.source_url,
        "source_text": result.source_text,
        "confidence": result.confidence,
        "explanation": result.explanation,
        "historical_deadlines": [
            {
                "conference_year": item.year,
                "deadline_utc": item.deadline.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
                "source": item.source,
            }
            for item in conference.ordered_history()
        ],
    }


if __name__ == "__main__":
    raise SystemExit(main())
