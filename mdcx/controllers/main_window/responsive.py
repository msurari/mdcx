"""Fit the interface to the REAL display, and keep it fitted when that changes.

The interface is built from absolute geometry (447 ``setGeometry`` calls) with no
reflow, so it only holds together at its design size of 1030x700. ``centralwidget``
is a plain absolute-positioned widget: the nav column sits at x=0..210 and the
``stackedWidget`` at x=210..1030.

The display is NOT 1030x700. Under jlesage's base image the X server runs a
virtual display whose size comes from ``DISPLAY_WIDTH``/``DISPLAY_HEIGHT`` in the
container environment (1200x750 on the live host, and v1 used the same). The app
never asked; it just pinned itself to its design size. So the window floated in a
mostly-empty desktop and every "does this text fit" measurement taken at an
invented size disagreed with what the user actually saw.

The contract now is:

* **Ask the screen.** The window and the scroll container take their size from the
  real screen, never from a hard-coded constant.
* **Never shrink below the design.** Absolute geometry is the design; going under
  1030x700 would push controls out of reach. Below that, the scroll area scrolls.
* **Re-adapt when the display changes.** VNC can be resized under a running app
  (and ``DISPLAY_WIDTH``/``DISPLAY_HEIGHT`` can be changed on the host), so the
  screen's ``geometryChanged`` signal re-runs the fit instead of leaving the
  window stuck at the size it happened to start with.
* **Nothing re-pins it.** ``MyMAinWindow.showEvent`` used to call
  ``resize(1030, 700)`` on every show, which put the window back at the design
  size after startup and made this fitting a no-op on any display that was not
  1030x700; it now calls :func:`fit_window_to_display` instead.

Deliberately additive: no .ui regeneration, no geometry rewritten, every
``Ui.<name>`` reference and every signal connection untouched -- the widgets are
reparented, and reparenting preserves both.

Why not convert to real layouts: those 447 absolute positions *are* the design,
and reflowing them is the vertical/portrait rebuild rather than a resize fix.
"""

from typing import List, Tuple

#: The window content was designed at this size (centralwidget's geometry).
DESIGN_SIZE: Tuple[int, int] = (1030, 700)

#: Widgets that must NOT scroll with the content: they are overlays shown on top
#: of the interface, positioned relative to the window rather than the content.
OVERLAYS: List[str] = ["widget_nfo"]


def real_display_size(window=None):
    """The size of the display the interface is ACTUALLY drawn into.

    Under jlesage's base image the X server is a virtual display sized by
    ``DISPLAY_WIDTH``/``DISPLAY_HEIGHT`` (1200x750 on the live host). This asks
    the screen, so the answer tracks reality instead of a constant, and it keeps
    tracking it after a VNC resize.

    Returns a QSize, or None when no screen can be determined.
    """
    from PyQt6.QtGui import QGuiApplication

    screen = None
    try:
        if window is not None:
            screen = window.screen()
    except Exception:
        screen = None
    if screen is None:
        screen = QGuiApplication.primaryScreen()
    if screen is None:
        return None
    return screen.availableGeometry().size()


def fit_size_for(window=None):
    """The size the scroll container should take: the display, never below design.

    Growing is free - the content is absolutely positioned from (0,0), so extra
    room only appears to the right and below and no control moves. Shrinking is
    not free: below DESIGN_SIZE the right-hand and lower controls would land
    outside the window, so the design size is the floor and the scroll area
    handles anything smaller.
    """
    from PyQt6.QtCore import QSize

    design_w, design_h = DESIGN_SIZE
    size = real_display_size(window)
    if size is None or not size.isValid():
        return design_w, design_h
    return max(design_w, size.width()), max(design_h, size.height())


def _resize_container(window, size=None) -> bool:
    """Re-apply the fitted size to the scroll container, when there is one."""
    from PyQt6.QtCore import QSize
    from PyQt6.QtWidgets import QWidget

    container = window.findChild(QWidget, "scrollContainer_window")
    if container is None:
        return False
    if size is None:
        size = fit_size_for(window)
    container.setFixedSize(QSize(size[0], size[1]))
    return True


def _hook_display_changes(window) -> None:
    """Re-fit when the display itself changes (VNC / ``DISPLAY_WIDTH``), once."""
    from PyQt6.QtGui import QGuiApplication

    if getattr(window, "_mdcx_display_hook", False):
        return
    screen = window.screen() or QGuiApplication.primaryScreen()
    if screen is None:
        return
    screen.geometryChanged.connect(lambda *_a: fit_window_to_display(window))
    window._mdcx_display_hook = True


def fit_window_to_display(window) -> bool:
    """Size the window, and its scroll container, from the display it is drawn into.

    The single entry point: ``main.py`` calls it once at startup and
    ``MyMAinWindow.showEvent`` calls it on every show, so no later resize can put
    the window back at the hard-coded design size. It is safe to call more than
    once and never raises -- a display that cannot be queried leaves the size
    alone rather than breaking startup.
    """
    try:
        size = fit_size_for(window)
        _resize_container(window, size)  # no-op when the scroll wrapper is absent
        window.resize(size[0], size[1])
        _hook_display_changes(window)
        return True
    except Exception:
        return False


def make_window_scrollable(window) -> bool:
    """Put the whole interface inside a scroll area.

    Returns True when the wrap was applied, False when it was already in place
    (so calling this twice is safe).
    """
    from PyQt6.QtCore import QSize
    from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

    central = window.centralWidget()
    if central is None:
        return False
    if central.layout() is not None:
        return False  # already wrapped

    # 1. the container takes the REAL display size, but never less than the design:
    #    every child's absolute geometry is preserved either way, because the
    #    origin stays (0,0) and growing only adds room to the right and bottom.
    width, height = fit_size_for(window)

    container = QWidget()
    container.setObjectName("scrollContainer_window")
    container.setFixedSize(QSize(width, height))

    # 2. move the content in. Reparenting keeps signal connections and keeps
    #    each child's geometry, since both parents share origin (0,0).
    for child in list(central.children()):
        if not isinstance(child, QWidget) or child.parent() is not central:
            continue
        if child.objectName() in OVERLAYS:
            continue
        child.setParent(container)

    # 3. the scroll area shows the container and scrolls when the window is
    #    smaller than the design size
    area = QScrollArea()
    area.setObjectName("scrollArea_window")
    area.setWidgetResizable(False)  # the container keeps its design size
    area.setWidget(container)

    # 4. the central widget now hosts the scroll area
    layout = QVBoxLayout(central)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(area)

    # 5. overlays stay children of central, floating above the scroll area
    for name in OVERLAYS:
        overlay = getattr(window.Ui, name, None)
        if overlay is not None and overlay.parent() is not central:
            overlay.setParent(central)
            overlay.raise_()

    return True
