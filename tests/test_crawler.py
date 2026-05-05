from datetime import timezone

from deadline_track.crawler import extract_deadline, html_to_text, parse_date


def test_html_to_text_ignores_hidden_content():
    text = html_to_text("<h1>Dates</h1><script>bad()</script><p>Submission deadline: March 7, 2026 AoE</p>")

    assert "Dates" in text
    assert "bad()" not in text
    assert "Submission deadline: March 7, 2026 AoE" in text


def test_parse_date_normalizes_to_utc():
    parsed = parse_date("March 7th, 2026 AoE")

    assert parsed is not None
    assert parsed.year == 2026
    assert parsed.month == 3
    assert parsed.day == 7
    assert parsed.tzinfo == timezone.utc


def test_extract_deadline_uses_deadline_context():
    text = (
        "Conference starts July 1, 2026. "
        "Important dates: paper submission deadline is March 7, 2026 AoE. "
        "Camera ready deadline is May 9, 2026."
    )

    deadline = extract_deadline(text, ("paper submission deadline", "submission deadline"))

    assert deadline is not None
    assert deadline.month == 3
    assert deadline.day == 7
