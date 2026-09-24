#!/usr/bin/env python3
"""Build the canonical, document-ordered list of unique .ui Han strings.

Ordering: file (MDCx.ui first), then first-occurrence line.
Writes /opt/data/profiles/movie/cache/scratch/canon.json  (list of records)
and  /opt/data/profiles/movie/cache/scratch/canon.txt     (review list, \\n-escaped)

The index in canon.json is the key used by the translation files
(tr_ui_*.py) so no Chinese key ever has to be re-typed by hand.
"""
import json
from pathlib import Path

data = json.load(open("/opt/data/profiles/movie/cache/scratch/ui_strings.json", encoding="utf-8"))
records = []
seen = {}
for rel in ("mdcx/views/MDCx.ui", "mdcx/views/posterCutTool.ui"):
    for r in data[rel]:
        if not r["han"]:
            continue
        v = r["value"]
        if v in seen:
            rec = seen[v]
            rec["occ"] += 1
            rec["all_lines"].append(r["line"])
            continue
        rec = {
            "idx": len(records),
            "value": v,
            "file": rel,
            "line": r["line"],
            "all_lines": [r["line"]],
            "context": r["context"],
            "widget": r["widget"],
            "widget_class": r["widget_class"],
            "property": r["property"],
            "in_item": r["in_item"],
            "occ": 1,
        }
        seen[v] = rec
        records.append(rec)

Path("/opt/data/profiles/movie/cache/scratch/canon.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8"
)

lines = [f"canonical unique .ui Han strings = {len(records)}"]
for rec in records:
    txt = rec["value"].replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r")
    lines.append(f"[{rec['idx']:3d}] ({rec['widget_class']} {rec['property']}) {txt}")
Path("/opt/data/profiles/movie/cache/scratch/canon.txt").write_text("\n".join(lines), encoding="utf-8")

occ = sum(r["occ"] for r in records)
print("unique:", len(records), "occurrences:", occ)
print("total chars:", sum(len(r["value"]) for r in records))
