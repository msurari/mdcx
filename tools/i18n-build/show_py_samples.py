#!/usr/bin/env python3
"""Print sample Chinese strings per file from the scan output."""
import json
import sys
from collections import Counter, defaultdict

payload = json.load(open("/opt/data/profiles/movie/cache/scratch/py_strings.json", encoding="utf-8"))
recs = payload["records"]

by_file = defaultdict(list)
for r in recs:
    by_file[r["file"]].append(r)

files = sys.argv[1:] if len(sys.argv) > 1 else sorted(by_file, key=lambda f: -len(by_file[f]))[:8]
for f in files:
    rs = by_file.get(f, [])
    uniq = len({r["value"] for r in rs})
    print(f"===== {f}  occ={len(rs)} uniq={uniq}")
    seen = set()
    n = 0
    for r in rs:
        if r["value"] in seen:
            continue
        seen.add(r["value"])
        n += 1
        if n > 40:
            break
        v = r["value"].replace("\n", "\\n")
        if len(v) > 90:
            v = v[:90] + "..."
        print(f"  {r['line']:5d} [{r['scope'][:38]:38s}] {v}")
    print()
