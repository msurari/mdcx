#!/usr/bin/env python3
"""Final on-disk verification of the phase-1 deliverables."""
import json
import re
import subprocess
from pathlib import Path

REPO = Path("/workspace/mdcx")
HAN = re.compile(r"[\u4e00-\u9fff]")

print("=== git status (repo) ===")
print(subprocess.run(["git", "-C", str(REPO), "status", "--short"], capture_output=True, text=True).stdout)
print("=== git diff --stat ===")
print(subprocess.run(["git", "-C", str(REPO), "diff", "--stat"], capture_output=True, text=True).stdout)

print("=== .ui files unchanged? ===")
for f in ("mdcx/views/MDCx.ui", "mdcx/views/posterCutTool.ui", "mdcx/views/MDCx.py",
          "mdcx/views/posterCutTool.py", "mdcx/config/models.py", "mdcx/config/enums.py"):
    out = subprocess.run(["git", "-C", str(REPO), "diff", "--stat", "--", f], capture_output=True, text=True).stdout
    print(f"  {f:38s} {'MODIFIED' if out.strip() else 'untouched'}")

print()
print("=== main.py diff ===")
print(subprocess.run(["git", "-C", str(REPO), "diff", "--", "main.py"], capture_output=True, text=True).stdout)

print("=== en.json ===")
en = json.loads((REPO / "mdcx/i18n/en.json").read_text(encoding="utf-8"))
print("  valid JSON, entries:", len(en))
print("  keys containing Han:", sum(1 for k in en if HAN.search(k)))
print("  values containing Han (untranslated leftovers):", sum(1 for v in en.values() if HAN.search(v)))
for k, v in en.items():
    if HAN.search(v):
        print("    ->", repr(k[:40]), "=", repr(v[:60]))
print("  duplicate keys: n/a (JSON object)")
print("  empty values:", sum(1 for v in en.values() if not v.strip()))
print()
print("=== files in mdcx/i18n ===")
for p in sorted((REPO / "mdcx/i18n").iterdir()):
    print(f"  {p.name:14s} {p.stat().st_size:8d} bytes")
print()
print("=== artifacts ===")
for p in sorted(Path("/workspace/team/movie/mdcx-i18n").rglob("*")):
    if p.is_file():
        print(f"  {p} ({p.stat().st_size} bytes)")
