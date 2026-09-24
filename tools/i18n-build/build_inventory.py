#!/usr/bin/env python3
"""Build /workspace/team/movie/mdcx-i18n/inventory.json + INVENTORY.md."""
import json
from collections import Counter
from pathlib import Path

HERE = Path("/opt/data/profiles/movie/cache/scratch")
DEST = Path("/workspace/team/movie/mdcx-i18n")
REPO = Path("/workspace/mdcx")

canon = json.load(open(HERE / "canon.json", encoding="utf-8"))
py = json.load(open(HERE / "py_classified.json", encoding="utf-8"))
labels = json.load(open(HERE / "settings_labels.json", encoding="utf-8"))
ui_scan = json.load(open(HERE / "ui_strings.json", encoding="utf-8"))
en = json.loads((REPO / "mdcx/i18n/en.json").read_text(encoding="utf-8"))
meta = json.loads((REPO / "mdcx/i18n/meta.json").read_text(encoding="utf-8"))
py_scan = json.load(open(HERE / "py_strings.json", encoding="utf-8"))

DEFERRED = {628}

# --- .ui ---------------------------------------------------------------------
ui_records = []
for rec in canon:
    e = {
        "idx": rec["idx"],
        "source": rec["value"],
        "file": rec["file"],
        "line": rec["line"],
        "context": rec["context"],
        "widget": rec["widget"],
        "widget_class": rec["widget_class"],
        "property": rec["property"],
        "occurrences_in_ui": rec["occ"],
        "class": "ui",
        "translated": rec["idx"] not in DEFERRED,
        "english": en.get(rec["value"]),
        "note": "deferred: 38.5k-char embedded help page" if rec["idx"] in DEFERRED else "",
    }
    ui_records.append(e)

ui_occ = sum(r["occ"] for r in canon)
ui_translated_unique = sum(1 for r in ui_records if r["translated"])
ui_translated_occ = sum(r["occurrences_in_ui"] for r in ui_records if r["translated"])

# --- .py ---------------------------------------------------------------------
py_records = []
for e in py["strings"]:
    py_records.append(
        {
            "source": e["value"],
            "class": e["category"],
            "in_ui_context": e["in_ui_context"],
            "in_data_context": e["in_data_context"],
            "locations": e["locations"][:8],
            "location_count": len(e["locations"]),
            "translated": False,
        }
    )
py_records.sort(key=lambda r: (r["class"], r["source"]))

# --- settings labels ---------------------------------------------------------
label_records = []
for e in sorted(labels["labels"], key=lambda x: x["value"]):
    label_records.append(
        {
            "label": e["value"],
            "class": "ui",
            "already_in_ui": e["in_ui"],
            "translated": bool(e["in_ui"] or en.get(e["value"])),
            "english": en.get(e["value"]),
            "sources": e["locations"],
            "note": "dropdown display name from a names() classmethod; names() is never called "
                    "anywhere in the app (dead code) -- the live dropdown labels come from the .ui"
            if e["locations"][0]["source"].endswith("enums.py") else
            "pydantic Field(title=...) metadata; no code path reads FieldInfo.title, so this label "
            "is not rendered by the current UI",
        }
    )

payload = {
    "meta": {
        "job": "MDCx English interface -- phase 1 (i18n layer + main-window translation)",
        "owner": "movie profile",
        "date": "2026-09-24",
        "upstream": "https://github.com/Hazard804/mdcx",
        "upstream_commit": "67a7ff78507f6f030439cd0b448fbdfc3e4f4a34",
        "upstream_release": "220260517",
        "local_clone": str(REPO),
        "translation_file": "mdcx/i18n/en.json",
        "translator": "mdcx/i18n/__init__.py (DictTranslator, installed from main.py)",
        "toolchain": "uv sync (PyQt6 6.11.0), QT_QPA_PLATFORM=offscreen",
    },
    "counts": {
        "ui_strings_unique": len(ui_records),
        "ui_strings_occurrences": ui_occ,
        "ui_strings_translated_unique": ui_translated_unique,
        "ui_strings_translated_occurrences": ui_translated_occ,
        "ui_strings_deferred": len(DEFERRED),
        "py_strings_scanned_files": py_scan["scanned_files"],
        "py_strings_excluded_files": py_scan["skipped_files"],
        "py_strings_unique": py["unique"],
        "py_strings_occurrences": py["occurrences"],
        "py_unique_by_class": py["unique_by_category"],
        "py_occurrences_by_class": py["occurrences_by_category"],
        "py_strings_translated": 0,
        "settings_labels_unique": len(label_records),
        "settings_labels_already_in_ui": sum(1 for r in label_records if r["already_in_ui"]),
        "settings_labels_translated": sum(1 for r in label_records if r["translated"]),
        "en_json_entries": len(en),
    },
    "excluded_from_scan": {
        "why": "site keywords / content, not interface -- translating them silently breaks scraping",
        "directories": ["mdcx/crawlers/", "tests/"],
        "files": ["mdcx/tools/wiki.py"],
        "also_excluded": [
            "mdcx/views/MDCx.py",
            "mdcx/views/posterCutTool.py",
        ],
        "also_excluded_why": "pyuic6-generated from the .ui files; their strings are the .ui "
                             "strings verbatim and are inventoried from the .ui instead",
    },
    "classification_rules": {
        "ui": "rendered to the user (a Qt setter/dialog/log call, an f-string message, a "
              "pydantic Field(title=...) settings label, or an enum names() display list)",
        "data": "site keyword, tag/genre value, filename/extension, separator, regex, or a "
                "literal inside a list/dict/set -- never translate",
        "unclassified": "seen in BOTH a ui and a data context, or in neither -- left in Chinese",
        "comment": "docstrings; never rendered, reported separately",
    },
    "ui_strings": ui_records,
    "py_strings": py_records,
    "settings_labels": label_records,
    "deferred": [
        {
            "what": "the embedded help page",
            "where": "mdcx/views/MDCx.ui (QTextBrowser, property html)",
            "size_chars": len(canon[628]["value"]),
            "why": "one single .ui string holding the entire upstream user manual in HTML; "
                   "out of proportion for phase 1 and documentation rather than chrome",
        }
    ],
}
(DEST / "inventory.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

# --- INVENTORY.md ------------------------------------------------------------
c = payload["counts"]
md = []
md.append("# MDCx i18n inventory (phase 1)")
md.append("")
md.append("Owner: **movie**. Date: 2026-09-24. Upstream `Hazard804/mdcx` @ "
          "`67a7ff78507f6f030439cd0b448fbdfc3e4f4a34` (release 220260517).")
md.append("Clone: `/workspace/mdcx` (the eventual fork is `msurari/mdcx`).")
md.append("")
md.append("`inventory.json` holds the machine-readable version of every table below.")
md.append("")
md.append("## Counts")
md.append("")
md.append("| what | unique | occurrences | translated |")
md.append("|---|---|---|---|")
md.append(f"| `.ui` Chinese strings (both files) | {c['ui_strings_unique']} | {c['ui_strings_occurrences']} | "
          f"{c['ui_strings_translated_unique']} unique / {c['ui_strings_translated_occurrences']} occurrences |")
md.append(f"| `.py` Chinese strings (UI-producing files) | {c['py_strings_unique']} | {c['py_strings_occurrences']} | "
          f"0 (see below) |")
md.append(f"| settings labels (models.py + enums.py) | {c['settings_labels_unique']} | - | "
          f"{c['settings_labels_translated']} |")
md.append(f"| `mdcx/i18n/en.json` entries | {c['en_json_entries']} | - | - |")
md.append("")
md.append("The `817` figure in the brief is the **occurrence** count of Chinese `.ui` strings: "
          f"{c['ui_strings_occurrences']} (797 in `MDCx.ui` + 20 in `posterCutTool.ui`). "
          f"The same strings de-duplicate to {c['ui_strings_unique']} unique keys, which is what a "
          "source-text keyed mapping needs.")
md.append("")
md.append("## `.ui` strings")
md.append("")
md.append(f"* {c['ui_strings_translated_unique']}/{c['ui_strings_unique']} unique strings translated "
          f"({c['ui_strings_translated_occurrences']}/{c['ui_strings_occurrences']} occurrences).")
md.append("* Deferred: **1** string, idx 628 — the embedded help page "
          "(`QTextBrowser`, property `html`, 38,574 characters: the whole upstream user manual in one "
          "HTML blob). It is documentation, not chrome, and is left in Chinese on purpose.")
md.append("* Contexts: `MDCx` (main window + settings, from `MDCx.ui`) and `Dialog_cut_poster` "
          "(`posterCutTool.ui`).")
md.append("* Every record in `inventory.json.ui_strings` carries its `widget`, `widget_class`, "
          "`property`, source `line` and its English value.")
md.append("")
md.append("## `.py` strings — classification")
md.append("")
md.append(f"Scanned **{c['py_strings_scanned_files']}** files, skipped **{c['py_strings_excluded_files']}**.")
md.append("")
md.append("| class | unique | occurrences | meaning |")
md.append("|---|---|---|---|")
for cls in ("ui", "data", "unclassified", "comment"):
    n = c["py_unique_by_class"].get(cls, 0)
    o = c["py_occurrences_by_class"].get(cls, 0)
    md.append(f"| `{cls}` | {n} | {o} | {payload['classification_rules'][cls]} |")
md.append("")
md.append("**None of these `.py` strings were translated in phase 1** — they are not routed through "
          "Qt's `translate()` today, so an entry in `en.json` would have no effect. Phase 1 covers the "
          "`.ui`-derived interface plus the settings vocabulary; wiring the remaining `.py` messages "
          "means calling `mdcx.i18n.tr()` at those call sites (phase 2 candidate).")
md.append("")
md.append("Excluded from the scan (hard rule): `mdcx/crawlers/*`, `mdcx/tools/wiki.py`, `tests/`, and "
          "the two `pyuic6`-generated view modules (their strings are the `.ui` strings).")
md.append("")
md.append("### Largest `ui`-classified files")
md.append("")
byfile = Counter(r["locations"][0]["file"] for r in py_records if r["class"] == "ui")
for f, n in byfile.most_common(10):
    md.append(f"* {n} — `{f}`")
md.append("")
md.append("### Largest `data`-classified files")
md.append("")
byfile = Counter(r["locations"][0]["file"] for r in py_records if r["class"] == "data")
for f, n in byfile.most_common(10):
    md.append(f"* {n} — `{f}`")
md.append("")
md.append("## Settings labels (`config/models.py`, `config/enums.py`)")
md.append("")
md.append(f"* {c['settings_labels_unique']} unique labels; "
          f"{c['settings_labels_already_in_ui']} already appear verbatim in the `.ui` (so they are "
          "covered by the `.ui` batch); "
          f"{c['settings_labels_unique'] - c['settings_labels_already_in_ui']} were added to `en.json`.")
md.append("* **Caveat, verified on disk:** nothing reads these labels. `FieldInfo.title` is never "
          "accessed anywhere in the app, and every `names()` classmethod in `config/enums.py` is dead "
          "code (no call site). The settings screen is hand-built in `MDCx.ui`, so its visible labels "
          "come from the `.ui` batch. The labels are in `en.json` so the vocabulary is ready, but they "
          "have **no runtime effect** yet.")
md.append("")
md.append("## Hard rule — never translated")
md.append("")
md.append("`mdcx/crawlers/*` (guochan.py, freejavbt.py, …), `mdcx/tools/wiki.py`, data-source names, "
          "tag/genre values, actor names, studio/series names, and anything matched against a website "
          "or written into the `.nfo`. Those files were excluded from the scan entirely and no entry "
          "was added for them.")
md.append("")
md.append("## Method (reproducible)")
md.append("")
md.append("1. `scan_ui.py` — parse both `.ui` files with `ElementTree`, keep every `<string>` whose text "
          "contains Han, record the widget `objectName`, widget class, property and line.")
md.append("2. `build_canon.py` — de-duplicate into document order → `canon.json` (659 records, idx = key).")
md.append("3. `scan_py.py` + `classify_py.py` — `ast` walk of every `.py` outside the excluded set, "
          "classify each Chinese literal by its AST context.")
md.append("4. `extract_settings_labels.py` — `Field(title=…)` and `names()` labels, minus what the `.ui` "
          "already has.")
md.append("5. Translation batches `tr_ui_a..e.py`, `tr_settings.py` — `{canon idx: english}` so no "
          "Chinese key is ever re-typed by hand.")
md.append("6. `build_en_json.py` — join batches against `canon.json` / `settings_labels.json` and write "
          "`mdcx/i18n/en.json` (+ `meta.json` provenance).")
md.append("7. `proof_i18n.py` — the acceptance test, output in `PROOF.txt`.")
md.append("")
md.append("All scripts are kept in `src/` next to this file.")
(DEST / "INVENTORY.md").write_text("\n".join(md) + "\n", encoding="utf-8")

print("wrote inventory.json + INVENTORY.md")
print(json.dumps(payload["counts"], ensure_ascii=False, indent=1))
