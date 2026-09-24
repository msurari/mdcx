#!/usr/bin/env python3
"""Split the canonical .ui string list into a short-line review file and a long-string file.

canon.txt      -- one line per unique string, values >400 chars replaced by a marker
canon_big.txt  -- the full text of every value >400 chars (\\n-escaped, one per line)
"""
import json
from pathlib import Path

recs = json.load(open("/opt/data/profiles/movie/cache/scratch/canon.json", encoding="utf-8"))

short, big = [], []
for r in recs:
    txt = r["value"].replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r")
    if len(r["value"]) > 400:
        big.append((r, txt))
        txt = f"<<{len(r['value'])} chars -- see canon_big.txt>>"
    short.append(f"[{r['idx']:3d}] ({r['widget_class']}/{r['property']}) {txt}")

Path("/opt/data/profiles/movie/cache/scratch/canon.txt").write_text("\n".join(short), encoding="utf-8")
biglines = [f"long strings = {len(big)}"]
for r, txt in big:
    biglines.append(f"[{r['idx']:3d}] ({r['widget_class']}/{r['property']}) len={len(r['value'])}")
    biglines.append(txt)
Path("/opt/data/profiles/movie/cache/scratch/canon_big.txt").write_text("\n".join(biglines), encoding="utf-8")
print("canon.txt lines:", len(short), "big:", len(big))
print("big idx:", [r["idx"] for r, _ in big])
print("chars in big:", sum(len(r["value"]) for r, _ in big))
