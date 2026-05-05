from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import re
from html.parser import HTMLParser
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import CrawlResult


DATE_PATTERNS = (
    r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
    r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|"
    r"Dec(?:ember)?)\.?\s+\d{1,2}(?:st|nd|rd|th)?[,]?\s+\d{4}"
    r"(?:\s*(?:AoE|UTC|GMT|PST|PDT|EST|EDT|CET|CEST))?",
    r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}"
    r"(?:\s*(?:AoE|UTC|GMT|PST|PDT|EST|EDT|CET|CEST))?",
    r"\b\d{1,2}[-/]\d{1,2}[-/]\d{4}"
    r"(?:\s*(?:AoE|UTC|GMT|PST|PDT|EST|EDT|CET|CEST))?",
)
DEADLINE_KEYWORDS = (
    "submission deadline",
    "paper deadline",
    "full paper deadline",
    "abstract deadline",
    "paper submission",
    "deadline",
)


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._hidden_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "noscript"}:
            self._hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript"} and self._hidden_depth:
            self._hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._hidden_depth:
            self.parts.append(data)

    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()


def fetch_page(url: str, timeout: int = 15) -> CrawlResult:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "deadline-track/0.1 "
                "(research deadline tracker; +https://github.com/phongtranr/deadline-track)"
            )
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read().decode(charset, errors="replace")
            last_modified = _parse_last_modified(response.headers.get("Last-Modified"))
            return CrawlResult(url=url, status="ok", text=html_to_text(body), last_modified=last_modified)
    except HTTPError as error:
        return CrawlResult(url=url, status=f"http_{error.code}", text="")
    except (OSError, URLError, TimeoutError) as error:
        return CrawlResult(url=url, status="error", text="", error=str(error))


def html_to_text(html: str) -> str:
    parser = VisibleTextParser()
    parser.feed(html)
    return parser.text()


def extract_deadline(text: str, track_keywords: Iterable[str] = DEADLINE_KEYWORDS) -> datetime | None:
    if not text:
        return None

    best: tuple[int, datetime] | None = None
    for date_match in _date_matches(text):
        context = _context(text, date_match.start(), date_match.end())
        keyword_score = _keyword_score(context, track_keywords)
        if keyword_score == 0:
            continue
        parsed = parse_date(date_match.group(0))
        if parsed is None:
            continue
        score = keyword_score - abs(len(context) // 2 - (date_match.start() - max(0, date_match.start() - 180)))
        if best is None or score > best[0]:
            best = (score, parsed)
    return best[1] if best else None


def parse_date(value: str) -> datetime | None:
    cleaned = re.sub(r"(\d)(st|nd|rd|th)", r"\1", value, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bAoE\b", "", cleaned, flags=re.IGNORECASE).strip(" ,")
    cleaned = re.sub(r"\s+", " ", cleaned)
    formats = (
        "%B %d, %Y",
        "%b %d, %Y",
        "%B %d %Y",
        "%b %d %Y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m-%d-%Y",
        "%m/%d/%Y",
    )
    for fmt in formats:
        try:
            return datetime.strptime(cleaned, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _date_matches(text: str) -> Iterable[re.Match[str]]:
    for pattern in DATE_PATTERNS:
        yield from re.finditer(pattern, text, flags=re.IGNORECASE)


def _context(text: str, start: int, end: int, width: int = 180) -> str:
    return text[max(0, start - width) : min(len(text), end + width)].lower()


def _keyword_score(context: str, keywords: Iterable[str]) -> int:
    score = 0
    for keyword in keywords:
        if keyword.lower() in context:
            score = max(score, len(keyword))
    return score


def _parse_last_modified(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)
