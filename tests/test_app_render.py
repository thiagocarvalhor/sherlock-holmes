"""Smoke test: the Streamlit app renders without raising (e.g. duplicate IDs).

Requires streamlit (the `webapp` extra). Skipped where streamlit is absent,
such as the lean CI environment that installs only the `dev` extra.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("streamlit")

from streamlit.testing.v1 import AppTest  # noqa: E402

APP = Path(__file__).resolve().parents[1] / "scripts" / "pncp_streamlit_app.py"


def test_app_renders_without_exception():
    at = AppTest.from_file(str(APP), default_timeout=30)
    at.run()
    assert not at.exception, f"App raised on render: {list(at.exception)}"


def test_app_has_two_tabs():
    at = AppTest.from_file(str(APP), default_timeout=30)
    at.run()
    labels = [t.label for t in at.tabs]
    assert any("Comparação" in label for label in labels)
    assert any("Busca" in label for label in labels)
