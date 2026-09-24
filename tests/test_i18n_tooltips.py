"""Hover descriptions must stay attached to real controls.

``apply_tooltips`` matches on objectName. If a control is renamed in the .ui and
the tooltip map is not updated, the description silently disappears -- the user
just sees no tooltip and nobody notices. This test fails in that case.

It also guards the six ``pushButton_tips_*`` buttons, whose tooltip IS the help
body rendered in a popup. Overwriting those with a one-liner would destroy real
help text, so that is asserted against explicitly.

Two traps this file has to avoid, both learned the hard way:
  * ``window.close()`` runs ``sys.exit()`` and kills the pytest process.
  * The window must stay referenced for the whole module -- a background
    cookie-check thread holds it and emits into it, so letting it be collected
    raises "wrapped C/C++ object ... has been deleted".
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

from mdcx.i18n.tooltips import (  # noqa: E402
    HELP_BODY_BUTTONS,
    TOOLTIPS,
    apply_tooltips,
)

#: keeps the window (and the QApplication) alive for the whole module
_ALIVE = []


@pytest.fixture(scope="module")
def window():
    from PyQt6.QtWidgets import QApplication

    from mdcx.controllers.main_window.main_window import MyMAinWindow

    app = QApplication.instance() or QApplication([])
    win = MyMAinWindow()
    _ALIVE.append((app, win))  # never closed: close() would run sys.exit()
    return win


def test_every_description_is_usable():
    assert TOOLTIPS, "tooltip map is empty"
    for name, text in TOOLTIPS.items():
        assert text.strip(), f"{name} has an empty description"
        assert len(text) <= 120, f"{name} too long for a hover bubble: {len(text)}"
        assert text.rstrip().endswith("."), f"{name} should be a sentence: {text!r}"


def test_widget_names_have_no_handler_suffix():
    """The `_clicked` suffix belongs to the slot, never to the widget."""
    bad = [n for n in TOOLTIPS if n.endswith("_clicked")]
    assert not bad, f"these keys look like handler names, not widget names: {bad}"


def test_help_body_buttons_are_not_in_the_map():
    overlap = sorted(set(TOOLTIPS) & set(HELP_BODY_BUTTONS))
    assert not overlap, f"these carry real help text and must stay out of the map: {overlap}"


def test_keys_match_real_controls(window):
    """Every key must name a control that exists in the built UI."""
    names = {w.objectName() for w in window.findChildren(object)}

    missing = sorted(n for n in TOOLTIPS if n not in names)
    assert not missing, f"tooltip keys match no control in the UI: {missing}"

    applied = apply_tooltips(window)
    assert applied > 0, "apply_tooltips set nothing"

    for name, text in TOOLTIPS.items():
        widgets = [w for w in window.findChildren(object) if w.objectName() == name]
        assert widgets, f"{name} not found"
        assert any(w.toolTip() == text for w in widgets), f"{name} tooltip not applied"


def test_help_body_tooltips_survive(window):
    """apply_tooltips must not shorten the six mode explanations."""
    def tip(n):
        return next(w for w in window.findChildren(object) if w.objectName() == n).toolTip()

    before = {n: tip(n) for n in HELP_BODY_BUTTONS}
    assert any(len(v) > 200 for v in before.values()), "expected long help bodies to exist"

    apply_tooltips(window)

    for name, original in before.items():
        assert tip(name) == original, f"{name} help body was overwritten by apply_tooltips"
