"""Smoke tests for the Streamlit app shell."""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("streamlit")

from streamlit.testing.v1 import AppTest  # noqa: E402

APP = Path(__file__).resolve().parents[3] / "scripts" / "pncp_streamlit_app.py"


def test_app_renders_without_exception():
    at = AppTest.from_file(str(APP), default_timeout=30)
    at.run()
    assert not at.exception, f"App raised on render: {list(at.exception)}"


def test_app_has_document_first_sections():
    at = AppTest.from_file(str(APP), default_timeout=30)
    at.run()
    headers = [header.value for header in at.header]
    assert headers == ["Documentos PNCP", "Comparacao manual"]
