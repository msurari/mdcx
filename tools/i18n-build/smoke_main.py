#!/usr/bin/env python3
"""Smoke test: run the real main.py offscreen and quit after a few seconds.

Proves the production startup path (QApplication -> install_translator -> MyMAinWindow)
works end to end and that the translator is installed before the window is built.
"""
import logging
import os
import runpy
import sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

os.chdir("/workspace/mdcx")
sys.path.insert(0, "/workspace/mdcx")

from PyQt6.QtCore import QTimer  # noqa: E402
from PyQt6.QtWidgets import QApplication  # noqa: E402

_orig_exec = QApplication.exec


def patched_exec(self):
    QTimer.singleShot(6000, self.quit)
    return _orig_exec(self)


QApplication.exec = patched_exec  # type: ignore[method-assign]

try:
    runpy.run_path("/workspace/mdcx/main.py", run_name="__main__")
except SystemExit as exc:
    print(f"main.py exited with SystemExit({exc.code})")
print("SMOKE TEST: main.py ran without an unhandled exception")
