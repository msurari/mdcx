#!/usr/bin/env python3
"""Probe: does Qt fall back to the source text when QTranslator.translate returns ""?"""
import json
from pathlib import Path

from PyQt6.QtCore import QCoreApplication, QTranslator
from PyQt6.QtWidgets import QApplication

en = json.loads(Path("/workspace/mdcx/mdcx/i18n/en.json").read_text(encoding="utf-8"))
print("en.json has '设置':", "设置" in en, repr(en.get("设置")))
print("en.json has ' 设置':", " 设置" in en, repr(en.get(" 设置")))
print("en.json has '开始':", repr(en.get("开始")))
print("keys starting with '设置':", [k for k in en if k.startswith("设置")])

app = QApplication([])


class Empty(QTranslator):
    def translate(self, context, source_text, disambiguation=None, n=-1):
        return ""


class NoneT(QTranslator):
    def translate(self, context, source_text, disambiguation=None, n=-1):
        return None


for name, t in (("returns ''", Empty()), ("returns None", NoneT())):
    app.installTranslator(t)
    got = QCoreApplication.translate("MDCx", "ABC_source")
    print(f"translator {name:14s}: translate('ABC_source') -> {got!r}  "
          f"{'FALLBACK OK' if got == 'ABC_source' else 'NO FALLBACK (blank!)'}")
    app.removeTranslator(t)

# and with no translator at all
print("no translator        : translate('ABC_source') ->", repr(QCoreApplication.translate("MDCx", "ABC_source")))
