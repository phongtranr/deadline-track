from __future__ import annotations

from datetime import datetime, timezone
from statistics import median

from .models import Conference


def predict_next_deadline(conference: Conference, now: datetime | None = None) -> tuple[datetime, str] | None:
    """Predict the next likely submission deadline from historical deadlines."""
    history = conference.ordered_history()
    if not history:
        return None

    now = now or datetime.now(timezone.utc)
    upcoming = [item.deadline for item in history if item.deadline > now]
    if upcoming:
        selected = min(upcoming)
        return selected, f"Using known historical deadline for {selected.year}."

    latest = history[-1]
    cadence = _conference_cadence_years(conference)
    next_year = latest.deadline.year + cadence
    while _replace_year_safely(latest.deadline, next_year) <= now:
        next_year += cadence

    predicted = _replace_year_safely(latest.deadline, next_year)
    return (
        predicted,
        f"Predicted from {len(history)} historical deadlines using a {cadence}-year cadence.",
    )


def _conference_cadence_years(conference: Conference) -> int:
    years = [item.year for item in conference.ordered_history()]
    if len(years) < 2:
        return 1

    gaps = [later - earlier for earlier, later in zip(years, years[1:]) if later > earlier]
    if not gaps:
        return 1
    return max(1, round(median(gaps)))


def _replace_year_safely(value: datetime, year: int) -> datetime:
    try:
        return value.replace(year=year)
    except ValueError:
        # Leap-day deadlines should roll to Feb 28 in non-leap years.
        return value.replace(year=year, day=28)
