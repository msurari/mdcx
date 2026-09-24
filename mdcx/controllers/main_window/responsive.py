"""Let the window be resized freely, with every control still reachable.

The interface is built from absolute geometry (447 ``setGeometry`` calls) with no
reflow, so it only holds together at its design size of 1030x700. ``centralwidget``
is a plain absolute-positioned widget: the nav column sits at x=0..210 and the
``stackedWidget`` at x=210..1030. Make the window narrower than 1030 and the
content does not reflow -- the right-hand and lower controls land outside the
window, where a click can never reach them.

The fix is the idiom two pages already use: ``page_tool`` and ``page_setting``
survive resizing because their content is inside a ``QScrollArea``. Here the same
treatment is applied once, at the top level, so the whole 1030x700 interface
scrolls inside whatever window size the user chooses.

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

    width, height = DESIGN_SIZE

    # 1. container keeps the design size, so every child's absolute geometry
    #    stays exactly as designed and nothing needs repositioning
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
