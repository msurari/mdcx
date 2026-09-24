#!/usr/bin/env python3
"""Assemble mdcx/i18n/en.json from the reviewed translation batches.

Sources (all under this directory):
  canon.json          - the 659 unique .ui Han strings (index = batch key)
  tr_ui_a..e.py       - {idx: english} for the .ui strings
  settings_labels.json- config/models.py + config/enums.py labels
  tr_settings.py      - {idx: english} for the labels the .ui does not carry

The Chinese keys are taken from canon.json / settings_labels.json verbatim, so no
Chinese source string is ever re-typed by hand.
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path("/workspace/mdcx")
OUT = REPO / "mdcx/i18n/en.json"

DEFERRED = {628}  # the 38,574-char embedded help page (QTextBrowser/html)


def load_mod(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.T


canon = json.load(open(HERE / "canon.json", encoding="utf-8"))
labels = json.load(open(HERE / "settings_labels.json", encoding="utf-8"))

ui_tr = {}
for name in ("tr_ui_a", "tr_ui_b", "tr_ui_c", "tr_ui_d", "tr_ui_e"):
    ui_tr.update(load_mod(HERE / f"{name}.py"))
set_tr = load_mod(HERE / "tr_settings.py")

mapping = {}
problems = []

# --- .ui strings -------------------------------------------------------------
for rec in canon:
    idx = rec["idx"]
    if idx in DEFERRED:
        continue
    if idx not in ui_tr:
        problems.append(f"ui idx {idx} has no translation: {rec['value'][:40]!r}")
        continue
    mapping[rec["value"]] = ui_tr[idx]

extra = set(ui_tr) - {r["idx"] for r in canon}
if extra:
    problems.append(f"translation indices not in canon: {sorted(extra)}")

# --- settings labels ---------------------------------------------------------
need = sorted(
    (e for e in labels["labels"] if not e["in_ui"]),
    key=lambda e: e["value"],
)
for i, e in enumerate(need):
    if i not in set_tr:
        problems.append(f"settings idx {i} has no translation: {e['value']!r}")
        continue
    mapping[e["value"]] = set_tr[i]

extra = set(set_tr) - set(range(len(need)))
if extra:
    problems.append(f"settings translation indices out of range: {sorted(extra)}")

# --- sanity ------------------------------------------------------------------
for k, v in mapping.items():
    if not isinstance(v, str) or not v.strip():
        problems.append(f"empty translation for {k!r}")

meta = {
    "generated_by": "movie profile, phase 1 (i18n layer + main-window translation)",
    "upstream": "https://github.com/Hazard804/mdcx",
    "upstream_commit": "67a7ff78507f6f030439cd0b448fbdfc3e4f4a34",
    "ui_strings_unique": len(canon),
    "ui_strings_translated": len(canon) - len(DEFERRED),
    "ui_strings_deferred": sorted(DEFERRED),
    "settings_labels_translated": len(need),
    "entries": len(mapping),
}

# en.json stays a pure flat {source: translation} mapping -- a source string may
# legitimately start with "_" (e.g. the .ui underscore-separator checkbox), so no key
# may be reserved. Provenance goes to meta.json instead.
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(dict(sorted(mapping.items())), ensure_ascii=False, indent=1) + "\n",
               encoding="utf-8")
(OUT.parent / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n",
                                      encoding="utf-8")

print(f"wrote {OUT}")
print(f"entries={len(mapping)} (ui {len(canon) - len(DEFERRED)}, settings {len(need)})")
print("problems:", len(problems))
for p in problems[:20]:
    print("  -", p)
