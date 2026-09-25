"""Give the English captions the room the Chinese ones did not need.

The main page is absolute-positioned, laid out for 2-3 character Chinese
captions. The field grid uses caption boxes of width 50 with the value
starting only 40px to the right:

    caption  x=30..80   value x=70      (label_director, label_studio, ...)
    caption  x=310..360 value x=350     (label_runtime, label_series, label_publish)

Chinese captions ("导演:", "发行商:") are ~26px and fit inside those 40px.
Their English equivalents are 52-59px, so they are clipped by the caption
box AND would overrun the value column: the live UI shows "Publishe" and
"Director" with the last glyph cut off.

Widen the caption box and push the value column right so the gap matches
what the English needs. Applied at startup rather than in the .ui so the
offsets stay in one tunable place and no regeneration is involved.

Additive by construction: only setGeometry, no reparenting, no signals
touched, no .ui or generated view rewritten.
"""

from PyQt6.QtWidgets import QWidget

#: Caption boxes are 50px wide; English needs room for the longest one
#: ("Publisher:" is ~59px at the base 12px font).
CAPTION_WIDTH = 62

#: Value column offsets. The caption must end before the value begins, so the
#: gap has to clear CAPTION_WIDTH plus a little breathing room.
VALUE_SHIFT = {
    70: 95,    # left column, mid page  (director / studio / release / tags)
    80: 95,    # left column, top page  (number / title / poster)
    350: 375,  # right column           (runtime / series / publisher)
}


def _resolve_page(target) -> "QWidget | None":
    """Accept either the controller (whose view lives on ``.Ui``) or a page widget.

    main.py holds the controller, not the view, and getting that wrong raises
    AttributeError during startup - which takes the whole app down for what is
    only a cosmetic layout tweak. Resolve defensively.
    """
    from PyQt6.QtWidgets import QWidget

    if target is None:
        return None
    if isinstance(target, QWidget):
        return target
    view = getattr(target, "Ui", None)
    return getattr(view, "page_main", None)


def widen_english_text_columns(target) -> int:
    """Widen caption boxes and shift value columns. Returns widgets touched.

    A cosmetic adjustment must never be able to stop the app from starting, so
    any failure here is swallowed after being reported.
    """
    try:
        return _widen_english_text_columns(target)
    except Exception:  # noqa: BLE001 - startup must survive a layout tweak
        import traceback

        traceback.print_exc()
        return 0


def _widen_english_text_columns(target) -> int:
    page = _resolve_page(target)
    if page is None:
        return 0
    touched = 0
    widgets = [w for w in page.findChildren(QWidget) if w.objectName()]

    # widen first, then shift, so the shift decision cannot be skewed by it
    for w in widgets:
        g = w.geometry()
        if g.width() == 50 and g.x() in (30, 310):
            w.setGeometry(g.x(), g.y(), CAPTION_WIDTH, g.height())
            touched += 1

    for w in widgets:
        g = w.geometry()
        if g.x() in VALUE_SHIFT:
            w.setGeometry(VALUE_SHIFT[g.x()], g.y(), g.width(), g.height())
            touched += 1

    return touched


# ---------------------------------------------------------------------------
# Text fitting: wrap and grow, never shrink the font.
#
# Measured on the live pages: the app is 1089px wide inside a ~1076px VNC
# viewport, so there is no horizontal room to widen the interface. But every
# page is a vertical QScrollArea with 200-3000px of UNUSED height below its
# content, and horizontal scrolling is switched off in 13 of the 14 of them.
# So the one axis with room to give is the vertical one.
#
# Reducing the font instead would need 9px (from 12px) to fit even the worst
# single label, and still would not fix the widest ones - while making every
# other string on every page hard to read.
#
# Therefore: let long text WRAP and grow downward, and stop Qt from crushing
# button labels into four-character stubs.
# ---------------------------------------------------------------------------

#: Extra pixels a label needs around its text so the last glyph is not clipped.
TEXT_PAD = 10

#: A button (checkbox/radio) draws its indicator to the LEFT of the label text, so
#: it needs that much more width than the text alone. Measuring with TEXT_PAD
#: under-reports every button by the indicator width and the last glyphs clip.
BUTTON_TEXT_PAD = 34

#: A checkbox label may claim at most this share of its row; beyond that the
#: help text would have no room left to wrap into.
BUTTON_WIDTH_SHARE = 0.62
BUTTON_RIGHT_MARGIN = 8


def _label_text(widget) -> str:
    """The widget's text with any HTML markup stripped."""
    import re

    raw = ""
    if hasattr(widget, "title") and hasattr(widget, "isCheckable"):
        pass
    if hasattr(widget, "text"):
        raw = widget.text() or ""
    elif hasattr(widget, "title"):
        raw = widget.title() or ""
    if not raw:
        return ""
    txt = re.sub(r"<[^>]+>", "", raw)
    return txt.replace("&nbsp;", " ").replace("&amp;", "&").strip()


def fit_english_text(target) -> int:
    """Wrap and grow every label whose English text does not fit. Returns count.

    Guarded for the same reason as the caption widening: a cosmetic pass must
    never be able to stop the app from starting.
    """
    try:
        return _fit_english_text(target)
    except Exception:  # noqa: BLE001 - startup must survive a layout tweak
        import traceback

        traceback.print_exc()
        return 0


def _fit_english_text(target) -> int:
    from PyQt6.QtGui import QFontMetrics
    from PyQt6.QtWidgets import QAbstractButton, QGroupBox, QLabel, QWidget

    from mdcx.controllers.main_window.english_layout import _resolve_page

    if target is None:
        return 0
    view = getattr(target, "Ui", target)
    pages = []
    for name in (
        "page_main", "page_log", "page_tool", "page_setting",
        "page_net", "page_about",
    ):
        pg = getattr(view, name, None)
        if pg is not None:
            pages.append(pg)
    if not pages:
        return 0

    touched = 0
    for page in pages:
        candidates = list(page.findChildren(QLabel))
        candidates += list(page.findChildren(QGroupBox))
        candidates += list(page.findChildren(QAbstractButton))

        for w in candidates:
            txt = _label_text(w)
            if not txt:
                continue
            # A label whose text already contains newlines is multi-line BY
            # DESIGN. horizontalAdvance() would measure all of it as one line
            # and report a wildly inflated width (up to 9,471px for a 500px
            # label), so leave those alone.
            if "\n" in txt:
                continue
            width = w.width()
            if width < 5:
                continue
            pad = BUTTON_TEXT_PAD if isinstance(w, QAbstractButton) else TEXT_PAD
            need = QFontMetrics(w.font()).horizontalAdvance(txt) + pad
            if need <= width:
                continue  # already fits

            # A checkbox/button label is the row's identity - it must never be
            # truncated to a stub. Claim up to its natural width, capped so the
            # neighbouring help text still has somewhere to wrap.
            if isinstance(w, QAbstractButton):
                # Cap on the width the row can actually give this widget: the
                # parent's remaining width to the right of the widget, less a
                # margin. A flat share of the parent is NOT enough - a button
                # placed far right overflows the parent even at its own natural
                # width, and Qt clips it at the parent's edge.
                parent = w.parentWidget()
                cap = need
                if parent is not None and parent.width() > 100:
                    room = parent.width() - w.geometry().x() - BUTTON_RIGHT_MARGIN
                    if room > 40:
                        cap = min(need, room)
                if cap > w.minimumWidth():
                    w.setMinimumWidth(cap)
                    touched += 1
                continue

            # Descriptive text: wrap it and give it the height the wrap needs.
            # The page has vertical room to spare; horizontal has none.
            if isinstance(w, QLabel) and not w.wordWrap():
                w.setWordWrap(True)
            if isinstance(w, QGroupBox):
                continue
            needed_h = w.heightForWidth(width)
            if needed_h > w.height():
                w.setMinimumHeight(needed_h)
            touched += 1

    return touched
