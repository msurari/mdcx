"""The interface translation must not change strings the code compares against.

MDCx decides what the Start button does by reading the button's own label:

    if self.Ui.pushButton_start_cap.text() == "开始":
        start_new_scrape(...)

Translating the label to "Start" without touching the comparison made the button a
no-op: neither the "开始" nor the "■ 停止" branch matched, so pressing Start did
nothing at all. Every such comparison now goes through ``mdcx.i18n.tr`` so the code
compares against the same value the widget displays.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

#: literals the controllers compare a widget's own text against
COMPARED = ["开始", "■ 停止", "开始检测", "停止检测"]


@pytest.mark.parametrize("literal", COMPARED)
def test_tr_matches_what_the_ui_displays(literal):
    """``tr(x)`` must equal what retranslateUi sets, because both call translate()."""
    qtcore = pytest.importorskip("PyQt6.QtCore")
    from mdcx.i18n import tr

    # this is exactly what the generated retranslateUi does for the .ui string
    displayed = qtcore.QCoreApplication.translate("MDCx", literal)
    assert tr(literal) == displayed


@pytest.mark.parametrize("literal", COMPARED)
def test_no_bare_literal_comparison_remains(literal):
    """A raw ``.text() == "<chinese>"`` would break again on translation."""
    offenders = []
    for py in (REPO / "mdcx").rglob("*.py"):
        for i, line in enumerate(py.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r'\.text\(\)\s*[!=]=\s*"' + re.escape(literal) + '"', line):
                offenders.append(f"{py.relative_to(REPO)}:{i}")
    assert not offenders, f"untranslated comparison of {literal!r}: {offenders}"
