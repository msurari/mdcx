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


def widen_english_text_columns(page: QWidget) -> int:
    """Widen caption boxes and shift value columns. Returns widgets touched."""
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
