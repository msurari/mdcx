"""The close/minimise "traffic light" buttons must stay invisible.

MDCx hides the real titlebar (``FramelessWindowHint``) and paints two 20x20
circles in the top-left corner as a substitute. In the container the window is
effectively fullscreen and its lifecycle belongs to the container, so there is
nothing for them to close or minimise -- they are decoration.

They are HIDDEN, never deleted: the generated view (``mdcx/views/MDCx.py``,
built from ``MDCx.ui``) still constructs them and its ``retranslateUi()`` still
calls ``setText()`` on them, so removing the widgets breaks startup. Same
pattern as ``pushButton_to_cut_2`` in ``cut_window.py``.

Measured independently on a real Xvfb display at 1200x750: the two rects go
from 165 x ``#F14C4C`` + 164 x ``#FFBC3C`` pixels to zero, and
``window.childAt(centre)`` returns ``close_widget`` in every window state.

The window is built offscreen exactly as ``tests/test_i18n_tooltips.py`` builds
it: it must stay referenced for the whole module (a background cookie-check
thread emits into it) and must never be closed (``close()`` runs ``sys.exit()``).
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

#: name -> the rect the generated .ui gives it (unchanged by the hide)
BUTTONS = {
    "pushButton_close": (10, 10, 20, 20),
    "pushButton_min": (35, 10, 20, 20),
}

_ALIVE = []


@pytest.fixture(scope="module")
def window():
    from PyQt6.QtWidgets import QApplication

    from mdcx.controllers.main_window.main_window import MyMAinWindow

    app = QApplication.instance() or QApplication([])
    win = MyMAinWindow()
    _ALIVE.append((app, win))  # never closed: close() would run sys.exit()
    return win


def _button(window, name):
    from PyQt6.QtWidgets import QPushButton

    btn = window.findChild(QPushButton, name)
    assert btn is not None, f"{name} is gone from the generated view"
    return btn


def test_widgets_still_exist_with_their_ui_geometry(window):
    """Hide, do not delete: the view still builds them and retranslateUi() uses them."""
    from PyQt6.QtWidgets import QWidget

    parent = window.findChild(QWidget, "close_widget")
    assert parent is not None, "close_widget (their parent) is gone"

    for name, rect in BUTTONS.items():
        btn = _button(window, name)
        assert btn.parent() is parent, f"{name} moved out of close_widget"
        g = btn.geometry()
        assert (g.x(), g.y(), g.width(), g.height()) == rect, (
            f"{name} geometry changed to {(g.x(), g.y(), g.width(), g.height())}; the hide must not resize anything"
        )
        assert btn.text().strip(), f"{name} lost its text - retranslateUi() still sets it"


def test_hidden_on_construction(window):
    for name in BUTTONS:
        btn = _button(window, name)
        assert btn.isHidden(), f"{name} is visible on construction"
        assert not btn.isVisibleTo(window), f"{name} is not explicitly hidden"


def test_hidden_in_every_window_state(window):
    """Both branches of the window-title adjust, plus hide/show of the window."""
    from mdcx.config.manager import manager

    original = manager.config.window_title
    try:
        for state in ("hide", "show"):
            manager.config.window_title = state
            window._windows_auto_adjust()
            for name in BUTTONS:
                btn = _button(window, name)
                assert not btn.isVisibleTo(window), f"{name} was shown by window_title={state!r}"
                assert btn.isHidden(), f"{name} is not explicitly hidden with window_title={state!r}"

        window.hide()
        window.show()
        for name in BUTTONS:
            assert _button(window, name).isHidden(), f"{name} came back after hide/show"
    finally:
        manager.config.window_title = original
        window._windows_auto_adjust()


def test_ctrl_m_shortcut_still_works(window):
    """Ctrl+M is bound to pushButton_min_clicked2 -- it must survive the hide."""
    from PyQt6.QtGui import QShortcut

    shortcuts = {s.key().toString(): s for s in window.findChildren(QShortcut)}
    assert "Ctrl+M" in shortcuts, f"the Ctrl+M shortcut is gone; found {sorted(shortcuts)}"

    shortcuts["Ctrl+M"].activated.emit()  # exactly what pressing Ctrl+M does

    for name in BUTTONS:
        assert _button(window, name).isHidden(), f"{name} reappeared after the Ctrl+M shortcut ran"
    window.showNormal()
