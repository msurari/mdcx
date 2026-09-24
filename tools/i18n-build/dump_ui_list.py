#!/usr/bin/env python3
"""Write a compact review list of the unique .ui Han strings to a text file."""
import json
from pathlib import Path

data = json.load(open("/opt/data/profiles/movie/cache/scratch/ui_strings.json", encoding="utf-8"))
uniq = {}
for rel, recs in data.items():
    for r in recs:
        if not r["han"]:
            continue
        v = r["value"]
        if v in uniq:
            uniq[v]["occ"] += 1
            uniq[v]["files"].add(rel.split("/")[-1])
            continue
        uniq[v] = {
            "occ": 1,
            "files": {rel.split("/")[-1]},
            "widget_class": r["widget_class"],
            "property": r["property"],
            "in_item": r["in_item"],
            "widget": r["widget"],
        }

items = sorted(uniq.items(), key=lambda kv: -len(kv[0]))
out = []
out.append(f"unique .ui Han strings = {len(items)}")
big = [(k, m) for k, m in items if len(k) > 400]
out.append(f"strings longer than 400 chars (HTML help blobs etc.) = {len(big)}  total chars={sum(len(k) for k,_ in big)}")
total_chars = sum(len(k) for k, _ in items)
out.append(f"total chars across all unique strings = {total_chars}")
out.append("")
out.append("idx | len | occ | widget_class | prop | item | preview")
for i, (k, m) in enumerate(items):
    prev = k.replace("\n", "\\n")[:110]
    out.append(f"{i:4d} | {len(k):5d} | {m['occ']:2d} | {str(m['widget_class'])[:18]:18s} | {str(m['property'])[:16]:16s} | {int(m['in_item'])} | {prev}")

Path("/opt/data/profiles/movie/cache/scratch/ui_strings_list.txt").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out[:6]))
print("written:", len(items), "lines")
