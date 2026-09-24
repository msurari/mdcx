#!/usr/bin/env python3
"""Extract every <string> from the two Qt Designer .ui files, with full context.

Output: /opt/data/profiles/movie/cache/scratch/ui_strings.json
Each record: file, context (<class> = the pyuic6 translate() context), widget (nearest
ancestor <widget name=>), widget_path (ancestor chain), widget_class, property (nearest
ancestor <property name=>), in_item (bool), value, han, line.

Uses lxml (a project dependency) because it reports the real source line of every
element. The 38.5 k-char help page is entity-encoded in the .ui, so locating its text by
a verbatim search does not work.
"""
import json
import re
from pathlib import Path

from lxml import etree

ROOT = Path("/workspace/mdcx")
UI_FILES = ["mdcx/views/MDCx.ui", "mdcx/views/posterCutTool.ui"]
OUT = Path("/opt/data/profiles/movie/cache/scratch/ui_strings.json")

HAN = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")


def walk(elem, state, out):
    tag = etree.QName(elem).localname
    st = dict(state)
    if tag == "widget":
        st["widget"] = elem.get("name") or st.get("widget")
        st["widget_class"] = elem.get("class") or st.get("widget_class")
        st["path"] = st.get("path", []) + [f"{st['widget_class']}:{st['widget']}"]
    elif tag == "property":
        st["property"] = elem.get("name")
    elif tag == "item":
        st["in_item"] = True
    elif tag == "string":
        val = elem.text or ""
        out.append(
            {
                "context": state["context"],
                "widget": st.get("widget"),
                "widget_path": " < ".join(st.get("path", [])),
                "widget_class": st.get("widget_class"),
                "property": st.get("property"),
                "in_item": bool(st.get("in_item")),
                "value": val,
                "han": bool(HAN.search(val)),
                "line": elem.sourceline,
            }
        )
        return
    for child in elem:
        walk(child, st, out)


def main():
    result = {}
    for rel in UI_FILES:
        p = ROOT / rel
        root = etree.parse(str(p)).getroot()
        out = []
        walk(root, {"context": root.findtext("class") or ""}, out)
        result[rel] = out
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    for rel, recs in result.items():
        han = [r for r in recs if r["han"]]
        missing = [r for r in recs if r["line"] is None]
        print(f"{rel}: strings={len(recs)} han_occ={len(han)} "
              f"han_unique={len({r['value'] for r in han})} without_line={len(missing)}")
    allhan = [r for recs in result.values() for r in recs if r["han"]]
    print("TOTAL han occ =", len(allhan), "unique =", len({r["value"] for r in allhan}))


if __name__ == "__main__":
    main()
