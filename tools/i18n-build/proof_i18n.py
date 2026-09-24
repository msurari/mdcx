#!/usr/bin/env python3
"""Phase-1 acceptance test: prove the translation resolves through Qt itself.

Run from the repo:
    QT_QPA_PLATFORM=offscreen uv run --project /workspace/mdcx python <this file>

Evidence:
  1. QCoreApplication.translate() on individual .ui strings.
  2. The real generated interface (mdcx.views.MDCx.Ui_MDCx) built on a QMainWindow: the
     live widget text is compared with en.json, so this checks what the user would see.
  3. Every unique .ui string resolved through Qt, counted (unique and occurrence-weighted,
     the 817 figure).
  4. The fallback: an untranslated string must come back as the original Chinese.
"""
from __future__ import annotations

import ast
import json
import os
import platform
import re
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path("/workspace/mdcx")
CANON = json.load(open(HERE / "canon.json", encoding="utf-8"))
EN = json.loads((REPO / "mdcx/i18n/en.json").read_text(encoding="utf-8"))
OUT = Path("/workspace/team/movie/mdcx-i18n/PROOF.txt")

lines: list[str] = []


def out(text: str = "") -> None:
    lines.append(text)
    print(text)


from PyQt6.QtCore import QCoreApplication, QT_VERSION_STR  # noqa: E402
from PyQt6.QtWidgets import QApplication, QMainWindow  # noqa: E402

from mdcx.i18n import current_translator, install_translator, load_translations  # noqa: E402

out("MDCx phase-1 acceptance test -- translation resolves through Qt")
out("=" * 74)
out(f"python            : {sys.version.split()[0]} ({platform.system()} {platform.machine()})")
out(f"PyQt6 / Qt        : {QT_VERSION_STR}")
out(f"QT_QPA_PLATFORM   : {os.environ.get('QT_QPA_PLATFORM', '(unset)')}")
out(f"MDCX_LANG         : {os.environ.get('MDCX_LANG', '(unset -> default en)')}")
out(f"repo              : {REPO}")
out(f"en.json entries   : {len(EN)}  (loaded by the package: {len(load_translations('en'))})")
out()

app = QApplication(sys.argv)
translator = install_translator(app)
out(f"install_translator(app) -> {translator!r}")
out(f"current_translator()    -> {current_translator()!r}")
out()

# --- 1. individual strings through Qt ---------------------------------------
out("1. QCoreApplication.translate(<context>, <.ui source string>)")
out("-" * 74)
samples = [CANON[i]["value"] for i in (0, 1, 20, 97, 322, 354, 357, 424, 622, 632)]
for s in samples:
    en = QCoreApplication.translate("MDCx", s)
    ok = bool(en) and en != s
    out(f"  {'OK ' if ok else '!! '} {s!r:30s} -> {en!r}")
out()

# --- 2. the real generated interface ----------------------------------------
out("2. the real generated interface (mdcx.views.MDCx.Ui_MDCx) on a QMainWindow")
out("   live widget text vs the en.json value for that source string")
out("-" * 74)
CALL = re.compile(r'self\.(\w+)\.(\w+)\(_translate\("MDCx", ("(?:[^"\\]|\\.)*")\)')
GETTER = {
    "setText": lambda w, m: w.text(),
    "setTitle": lambda w, m: w.title(),
    "setToolTip": lambda w, m: w.toolTip(),
    "setPlaceholderText": lambda w, m: w.placeholderText(),
}
HAN = re.compile(r"[\u4e00-\u9fff]")
ui_ok = False
try:
    from mdcx.views.MDCx import Ui_MDCx

    window = QMainWindow()
    ui = Ui_MDCx()
    ui.setupUi(window)
    ui_ok = True

    calls = []
    for line in (REPO / "mdcx/views/MDCx.py").read_text(encoding="utf-8").splitlines():
        m = CALL.search(line)
        if not m or m.group(2) not in GETTER:
            continue
        source = ast.literal_eval(m.group(3))  # undo the \n / \" escapes of the literal
        if HAN.search(source):
            calls.append((m.group(1), m.group(2), source))
    # deterministic spread over the whole generated file
    step = max(1, len(calls) // 12)
    checked = matched = 0
    for attr, method, source in calls[::step][:12]:
        widget = getattr(ui, attr, None)
        if widget is None:
            continue
        live = GETTER[method](widget, method)
        expected = EN.get(source)
        checked += 1
        ok = live == expected
        matched += ok
        out(f"  {'OK ' if ok else '!! '} {attr}.{method:18s} live={live!r:48s} en.json={expected!r}")
    out(f"  checked {matched}/{checked} live widgets against en.json")
    out(f"  window title = {window.windowTitle()!r}")
except Exception:  # noqa: BLE001
    out("  !! could not build the generated interface:")
    out("  " + traceback.format_exc().replace("\n", "\n  "))
out()

# --- 3. count every .ui string through Qt -----------------------------------
out("3. every unique .ui string, resolved through Qt")
out("-" * 74)
resolved_unique = 0
resolved_occ = 0
total_occ = 0
unresolved = []
for rec in CANON:
    total_occ += rec["occ"]
    en = QCoreApplication.translate(rec["context"], rec["value"])
    if en and en != rec["value"]:
        resolved_unique += 1
        resolved_occ += rec["occ"]
    else:
        unresolved.append(rec)

out(f"  unique .ui Han strings            : {len(CANON)}")
out(f"  resolved (English returned)       : {resolved_unique}")
out(f"  unresolved                        : {len(unresolved)}")
out(f"  .ui occurrences (the 817 figure)  : {total_occ}")
out(f"  occurrences resolved              : {resolved_occ}")
out()
if unresolved:
    out("  unresolved strings (deliberately left in Chinese):")
    for rec in unresolved:
        out(f"    idx {rec['idx']:3d}  {rec['file'].split('/')[-1]}:{rec['line']}  "
            f"{rec['widget_class']}/{rec['property']}  len={len(rec['value'])}")
    out()

# --- 4. fallback behaviour ---------------------------------------------------
out("4. fallback: a string with no entry must come back as the original Chinese")
out("-" * 74)
missing = "这个字符串肯定没有翻译"
back = QCoreApplication.translate("MDCx", missing)
out(f"  translate({missing!r}) -> {back!r}  "
    f"{'OK (fell back to the source)' if back == missing else '!! NOT the source text'}")
out("  (returning \"\" from QTranslator.translate does NOT fall back on PyQt6 6.11 --")
out("   it blanks the widget; the translator therefore returns the source text)")
out(f"  translator hits/misses this run: "
    f"{translator.hits if translator else 'n/a'}/{translator.misses if translator else 'n/a'}")
out()

out("VERDICT")
out("-" * 74)
out(f"  interface built from the .ui files  : {'yes' if ui_ok else 'no'}")
out(f"  English rendered through Qt         : {'yes' if resolved_unique else 'no'}")
out(f"  .ui unique coverage                 : {resolved_unique}/{len(CANON)}")
out(f"  .ui occurrence coverage             : {resolved_occ}/{total_occ}")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"\nwritten: {OUT}")
