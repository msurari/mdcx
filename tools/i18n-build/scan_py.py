#!/usr/bin/env python3
"""Scan the MDCx tree for Chinese string literals in UI-producing .py files.

Excludes (per JOB-MDCX-ENGLISH.md hard rule):
  mdcx/crawlers/*      -> site keywords / scraping logic
  mdcx/tools/wiki.py   -> site keyword handling
  tests/*              -> not shipped UI
Also excludes the pyuic6-generated views (MDCx.py / posterCutTool.py) because their
strings are the .ui strings verbatim -- they are inventoried from the .ui instead.
"""
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path("/workspace/mdcx")
OUT = Path("/opt/data/profiles/movie/cache/scratch/py_strings.json")

CJK = re.compile(r"[\u3000-\u303f\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef]")

EXCLUDE_DIRS = ("mdcx/crawlers", "tests")
EXCLUDE_FILES = ("mdcx/tools/wiki.py", "mdcx/views/MDCx.py", "mdcx/views/posterCutTool.py")


def is_excluded(rel: str) -> bool:
    if rel in EXCLUDE_FILES:
        return True
    return any(rel.startswith(d + "/") for d in EXCLUDE_DIRS)


class Visitor(ast.NodeVisitor):
    def __init__(self, rel, src_lines):
        self.rel = rel
        self.src = src_lines
        self.stack = []
        self.records = []

    def _scope(self):
        return ".".join(self.stack) if self.stack else "<module>"

    def visit_ClassDef(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Constant(self, node):
        if isinstance(node.value, str) and CJK.search(node.value):
            self.records.append(
                {
                    "file": self.rel,
                    "line": node.lineno,
                    "scope": self._scope(),
                    "value": node.value,
                    "kind": "str",
                }
            )
        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        for part in node.values:
            if isinstance(part, ast.Constant) and isinstance(part.value, str) and CJK.search(part.value):
                self.records.append(
                    {
                        "file": self.rel,
                        "line": node.lineno,
                        "scope": self._scope(),
                        "value": part.value,
                        "kind": "fstring-part",
                    }
                )
        self.generic_visit(node)


def main():
    files = sorted(ROOT.rglob("*.py"))
    records = []
    scanned = []
    skipped = []
    errors = []
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        if rel.startswith(".venv/") or "/.venv/" in rel:
            continue
        if is_excluded(rel):
            skipped.append(rel)
            continue
        try:
            src = f.read_text(encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            errors.append({"file": rel, "error": repr(e)})
            continue
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            errors.append({"file": rel, "error": f"SyntaxError {e}"})
            continue
        scanned.append(rel)
        v = Visitor(rel, src.splitlines())
        v.visit(tree)
        records.extend(v.records)

    # dedupe view for counting
    uniq = {}
    for r in records:
        uniq.setdefault(r["value"], []).append({"file": r["file"], "line": r["line"], "scope": r["scope"]})

    payload = {
        "scanned_files": len(scanned),
        "skipped_files": len(skipped),
        "skipped_list": skipped,
        "parse_errors": errors,
        "occurrences": len(records),
        "unique": len(uniq),
        "records": records,
        "unique_map": uniq,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"scanned={len(scanned)} skipped={len(skipped)} errors={len(errors)}")
    print(f"occurrences={len(records)} unique={len(uniq)}")
    print("top files by occurrences:")
    from collections import Counter

    c = Counter(r["file"] for r in records)
    for k, n in c.most_common(20):
        print(f"  {n:5d}  {k}")
    print("errors:", errors[:5])


if __name__ == "__main__":
    sys.exit(main())
