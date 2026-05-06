from __future__ import annotations

from pathlib import Path


def test_static_site_refresh_button_is_wired_to_data_reload() -> None:
    html = Path("docs/index.html").read_text(encoding="utf-8")
    script = Path("docs/app.js").read_text(encoding="utf-8")

    assert 'id="refresh-data"' in html
    assert 'id="refresh-status"' in html
    assert 'src="./app.js?v=' in html
    assert 'querySelector("#refresh-data")' in script
    assert '"click"' in script
    assert "event.preventDefault()" in script
    assert "loadDeadlineData()" in script
    assert "loadDeadlineData({ disableRefreshButton: false })" in script
    assert "?ts=${Date.now()}" in script
