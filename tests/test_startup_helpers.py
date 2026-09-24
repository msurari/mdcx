"""The post-setup helpers main.py calls, with the argument main.py actually passes.

Regression test: widen_english_text_columns() was written to take the view
(ui.page_main), but main.py holds the CONTROLLER (MyMAinWindow), whose view lives
on .Ui. The mismatch raised AttributeError at import time, so the container
crash-looped and its VNC port flapped.

The full controller is not constructed here - it starts background threads and
does network work, which makes for a fragile, slow test. Instead the call-site
text in main.py is asserted directly and the resolver is driven with objects of
the same SHAPE, which is precisely what the bug was about.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

pytest.importorskip("PyQt6")

from PyQt6.QtWidgets import QApplication, QWidget  # noqa: E402


@pytest.fixture(scope="module")
def app():
    yield QApplication.instance() or QApplication([])


def test_main_py_passes_the_controller_not_the_view():
    """Guard the call site: main.py must pass the object it actually holds."""
    src = (Path(__file__).resolve().parent.parent / "main.py").read_text(encoding="utf-8")
    assert "widen_english_text_columns(ui)" in src, (
        "main.py must pass the controller; passing ui.page_main crashed startup"
    )
    assert "widen_english_text_columns(ui.page_main)" not in src


def test_resolves_a_controller_shape(app):
    """The controller exposes the view on .Ui - this is what broke."""
    from mdcx.controllers.main_window.english_layout import _resolve_page

    page = QWidget()

    class View:
        page_main = page

    class Controller:
        Ui = View()

    assert _resolve_page(Controller()) is page


def test_resolves_a_bare_page(app):
    from mdcx.controllers.main_window.english_layout import _resolve_page

    page = QWidget()
    assert _resolve_page(page) is page


def test_resolves_none_and_missing_attributes(app):
    from mdcx.controllers.main_window.english_layout import _resolve_page

    assert _resolve_page(None) is None
    assert _resolve_page(object()) is None          # no .Ui at all
    assert _resolve_page(type("V", (), {"Ui": object()})()) is None  # .Ui but no page_main


def test_widen_never_raises_and_returns_zero_on_bad_target():
    """A cosmetic tweak must never be able to stop the app from starting."""
    from mdcx.controllers.main_window.english_layout import widen_english_text_columns

    class Hostile:
        @property
        def Ui(self):
            raise RuntimeError("boom")

    assert widen_english_text_columns(Hostile()) == 0
    assert widen_english_text_columns(None) == 0
    assert widen_english_text_columns(object()) == 0


def test_widen_runs_against_a_real_page(app):
    """End-to-end through the real function on a real widget."""
    from mdcx.controllers.main_window.english_layout import widen_english_text_columns

    page = QWidget()
    page.setObjectName("page_main")
    assert isinstance(widen_english_text_columns(page), int)
