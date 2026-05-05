from __future__ import annotations

from pathlib import Path


def test_pages_workflow_can_enable_pages_on_first_deploy() -> None:
    workflow = Path(".github/workflows/pages.yml").read_text(encoding="utf-8")

    assert "uses: actions/configure-pages@v5" in workflow
    assert "enablement: true" in workflow

