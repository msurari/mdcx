#!/usr/bin/env python3
"""Extract the settings labels from config/models.py (Field(title=...)) and
config/enums.py (names() display lists), minus anything the .ui already carries.

Writes /opt/data/profiles/movie/cache/scratch/settings_labels.json
"""
import ast
import json
import re
from pathlib import Path

ROOT = Path("/workspace/mdcx")
OUT = Path("/opt/data/profiles/movie/cache/scratch/settings_labels.json")
CJK = re.compile(r"[\u3000-\u303f\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef]")

canon = json.load(open("/opt/data/profiles/movie/cache/scratch/canon.json", encoding="utf-8"))
ui_values = {r["value"] for r in canon}

records = []


def add(value, source, where):
    if not CJK.search(value):
        return
    records.append({"value": value, "source": source, "where": where})


# --- models.py: Field(title=...) -------------------------------------------------
src = (ROOT / "mdcx/config/models.py").read_text(encoding="utf-8")
tree = ast.parse(src)
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Field":
        for kw in node.keywords:
            if kw.arg == "title" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                add(kw.value.value, "mdcx/config/models.py", f"Field(title=) line {kw.value.lineno}")

# --- enums.py: names() lists ------------------------------------------------------
src2 = (ROOT / "mdcx/config/enums.py").read_text(encoding="utf-8")
tree2 = ast.parse(src2)
for cls in [n for n in ast.walk(tree2) if isinstance(n, ast.ClassDef)]:
    for fn in [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "names"]:
        for node in ast.walk(fn):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                add(node.value, "mdcx/config/enums.py", f"{cls.name}.names() line {node.lineno}")

# de-duplicate, keep every source location
merged = {}
for r in records:
    e = merged.setdefault(r["value"], {"value": r["value"], "locations": [], "in_ui": r["value"] in ui_values})
    e["locations"].append({"source": r["source"], "where": r["where"]})

need = {k: v for k, v in merged.items() if not v["in_ui"]}
have = {k: v for k, v in merged.items() if v["in_ui"]}
payload = {
    "settings_labels_total": len(merged),
    "already_in_ui": len(have),
    "not_in_ui": len(need),
    "labels": sorted(merged.values(), key=lambda e: e["value"]),
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"settings labels: total={len(merged)} already covered by .ui={len(have)} need translation={len(need)}")
print("\n-- not in .ui (need translation) --")
for i, k in enumerate(sorted(need)):
    print(f"{i:4d} | {k}")
