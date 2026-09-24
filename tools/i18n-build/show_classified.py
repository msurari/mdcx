import json
import sys
from collections import Counter, defaultdict

p = json.load(open("/opt/data/profiles/movie/cache/scratch/py_classified.json", encoding="utf-8"))
cat = sys.argv[1] if len(sys.argv) > 1 else "data"
n = int(sys.argv[2]) if len(sys.argv) > 2 else 60
items = [e for e in p["strings"] if e["category"] == cat]
print(f"category={cat} unique={len(items)}")
for e in items[:n]:
    loc = e["locations"][0]
    v = e["value"].replace("\n", "\\n")[:80]
    print(f"  [{loc['file']}:{loc['line']}] {v}")
print()
print("per-file counts for this category:")
c = Counter(e["locations"][0]["file"] for e in items)
for k, v in c.most_common(15):
    print(f"  {v:5d}  {k}")
