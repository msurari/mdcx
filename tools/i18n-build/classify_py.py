#!/usr/bin/env python3
"""Classify every Chinese string literal in the UI-producing .py files.

Categories
  ui           - interface chrome / a message shown to the user  -> translatable
  data         - site keywords, tag/genre values, filenames, separators, regex,
                 anything matched against a site or written into the .nfo -> NEVER translate
  unclassified - cannot be told apart from the AST context alone -> left in Chinese
  comment      - docstrings (never rendered); reported separately, not part of the
                 ui/data/unclassified split

Writes /opt/data/profiles/movie/cache/scratch/py_classified.json
"""
import ast
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path("/workspace/mdcx")
SCAN = Path("/opt/data/profiles/movie/cache/scratch/py_strings.json")
OUT = Path("/opt/data/profiles/movie/cache/scratch/py_classified.json")

UI_CALLS = {
    # Qt widgets / dialogs -> user-visible text
    "setText", "setWindowTitle", "setToolTip", "setStatusTip", "setWhatsThis", "setPlaceholderText",
    "setTitle", "addItem", "addItems", "setItemText", "setHeaderLabel", "setTabText", "setAccessibleDescription",
    "setAccessibleName", "setHtml", "setPlainText", "appendPlainText", "showMessage", "setWindowFilePath",
    "information", "warning", "critical", "question", "about", "setLabelText", "setInformativeText",
    "setDetailedText", "setTextFormat",
    # logging / console messages
    "print", "info", "debug", "warning_", "error", "critical_", "exception", "log", "append", "write",
    "add_row", "add_line", "set_message", "update_status",
}
DATA_HINT_NAMES = re.compile(
    r"(mapping|map_|_map|dict|tags?|genres?|keyword|site|url|host|regex|pattern|suffix|prefix|ext|"
    r"replace|split|strip|clean|ignore|exclude|wuma|youma|suren|oumei|guochan|mosaic|leak|umr|"
    r"field_names?|values?|names_|lang|headers?)",
    re.I,
)
UI_HINT_NAMES = re.compile(r"(msg|message|text|title|label|hint|tip|info|prompt|desc|warning|error)", re.I)

CJK = re.compile(r"[\u3000-\u303f\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef]")

# functions whose string arguments are data, not chrome
DATA_FUNCS = {
    "re.compile", "compile", "match", "search", "fullmatch", "sub", "findall", "finditer", "split",
    "startswith", "endswith", "join", "get", "setdefault", "add", "update", "extend", "append_",
    "translate", "maketrans", "replace",
}


class Collector(ast.NodeVisitor):
    def __init__(self, rel, tree):
        self.rel = rel
        self.tree = tree
        self.records = []
        self.docstrings = set()
        self.stack = []

    def _collect_docstrings(self):
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                ds = ast.get_docstring(node, clean=False)
                if ds:
                    self.docstrings.add((node.lineno, ds))

    def run(self):
        self._collect_docstrings()
        self.visit(self.tree)
        return self.records

    def visit_ClassDef(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    # --- helpers -------------------------------------------------------
    def _parent_of(self, target):
        for node in ast.walk(self.tree):
            for child in ast.iter_child_nodes(node):
                if child is target:
                    return node
        return None

    def _add(self, node, value, kind, parents):
        self.records.append(
            {
                "file": self.rel,
                "line": node.lineno,
                "scope": ".".join(self.stack) if self.stack else "<module>",
                "value": value,
                "kind": kind,
                "parents": parents,
            }
        )


def classify(rec, parents):
    """parents: list of parent node type names from nearest to farthest."""
    p = parents[0] if parents else ""
    kinds = set(parents)
    if rec["kind"] == "docstring":
        return "comment"
    # enum display-name lists (Settings dropdown labels) are interface, not data
    if rec["file"].endswith("config/enums.py") and rec.get("scope", "").endswith("names"):
        return "ui"
    if "Compare" in kinds or "UnaryOp" in kinds:
        return "data"
    if "re.compile" in kinds or "pattern" in (rec.get("call") or ""):
        return "data"
    if rec["kind"] == "fstring-part":
        return "ui"
    if p == "keyword" and rec.get("kw") == "title":
        return "ui"
    if rec.get("call") == "Field" and rec.get("assign_name") in ("default", "default_factory"):
        return "data"
    if rec.get("call") in UI_CALLS:
        return "ui"
    if p in ("Dict", "List", "Tuple", "Set"):
        return "data"
    if rec.get("call") in DATA_FUNCS:
        return "data"
    if rec.get("assign_name") and UI_HINT_NAMES.search(rec["assign_name"]):
        return "ui"
    return "unclassified"


def analyse(rel, tree, src_lines):
    """Walk and produce records with parent/call context."""
    out = []

    doc_ranges = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            ds = ast.get_docstring(node, clean=False)
            if ds:
                body = node.body
                if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                    doc_ranges.append((body[0].value.lineno, body[0].value.end_lineno, ds))

    def is_docstring(node):
        return any(a <= node.lineno <= b for a, b, _ in doc_ranges)

    class W(ast.NodeVisitor):
        def __init__(self):
            self.parents = []
            self.scope = []

        def visit_ClassDef(self, node):
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        def visit_FunctionDef(self, node):
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

        def _emit(self, node, value, kind, call=None, kw=None, assign_name=None):
            if not CJK.search(value):
                return
            out.append(
                {
                    "file": rel,
                    "line": node.lineno,
                    "scope": ".".join(self.scope) if self.scope else "<module>",
                    "value": value,
                    "kind": kind,
                    "parents": [type(x).__name__ for x in reversed(self.parents[-6:])],
                    "call": call,
                    "kw": kw,
                    "assign_name": assign_name,
                    "docstring": is_docstring(node),
                }
            )

        def _call_name(self, node):
            f = node.func
            if isinstance(f, ast.Attribute):
                return f.attr
            if isinstance(f, ast.Name):
                return f.id
            return ""

        def _assign_name(self):
            for x in reversed(self.parents):
                if isinstance(x, ast.Assign):
                    for t in x.targets:
                        if isinstance(t, ast.Name):
                            return t.id
                        if isinstance(t, ast.Attribute):
                            return t.attr
                if isinstance(x, ast.AnnAssign) and isinstance(x.target, ast.Name):
                    return x.target.id
                if isinstance(x, ast.keyword) and x.arg:
                    return x.arg
            return None

        def visit_Call(self, node):
            self.parents.append(node)
            call = self._call_name(node)
            prev = getattr(self, "_cur_call", None)
            self._cur_call = call
            for child in ast.iter_child_nodes(node):
                self.visit(child)
            self._cur_call = prev
            self.parents.pop()

        def visit_keyword(self, node):
            self.parents.append(node)
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                self._emit(node.value, node.value.value, "str", kw=node.arg, assign_name=self._assign_name())
            self.visit(node.value) if not isinstance(node.value, ast.Constant) else None
            self.parents.pop()

        def visit_Dict(self, node):
            self.parents.append(node)
            self.generic_visit(node)
            self.parents.pop()

        def visit_List(self, node):
            self.parents.append(node)
            self.generic_visit(node)
            self.parents.pop()

        visit_Tuple = visit_List
        visit_Set = visit_List

        def visit_Lambda(self, node):
            self.parents.append(node)
            self.generic_visit(node)
            self.parents.pop()

        def visit_Assign(self, node):
            self.parents.append(node)
            self.generic_visit(node)
            self.parents.pop()

        def visit_Constant(self, node):
            if isinstance(node.value, str) and node.value.strip():
                cur_call = getattr(self, "_cur_call", None)
                self._emit(node, node.value, "docstring" if is_docstring(node) else "str",
                           call=cur_call, assign_name=self._assign_name())

        def visit_JoinedStr(self, node):
            self.parents.append(node)
            for part in node.values:
                if isinstance(part, ast.Constant) and isinstance(part.value, str) and part.value.strip():
                    self._emit(part, part.value, "fstring-part", call=getattr(self, "_cur_call", None),
                               assign_name=self._assign_name())
            for part in node.values:
                if not isinstance(part, ast.Constant):
                    self.visit(part)
            self.parents.pop()

    W().visit(tree)
    return out


def main():
    scan = json.load(open(SCAN, encoding="utf-8"))
    files = sorted({r["file"] for r in scan["records"]})
    all_recs = []
    for rel in files:
        src = (ROOT / rel).read_text(encoding="utf-8")
        tree = ast.parse(src)
        all_recs.extend(analyse(rel, tree, src.splitlines()))

    for r in all_recs:
        r["category"] = classify(r, r["parents"])

    # de-duplicate per (value) for the inventory, keeping every location
    uniq = {}
    for r in all_recs:
        key = r["value"]
        e = uniq.setdefault(key, {"value": key, "category": r["category"], "locations": [], "cats": Counter()})
        e["locations"].append({"file": r["file"], "line": r["line"], "scope": r["scope"], "call": r["call"]})
        e["cats"][r["category"]] += 1

    # aggregate per string: conservative rule
    #   data-context only          -> data
    #   ui-context only            -> ui
    #   both (ambiguous)           -> unclassified
    #   neither                    -> unclassified
    for e in uniq.values():
        e["in_data_context"] = bool(e["cats"].get("data"))
        e["in_ui_context"] = bool(e["cats"].get("ui"))
        if set(e["cats"]) == {"comment"}:
            e["category"] = "comment"
        elif e["in_data_context"] and not e["in_ui_context"]:
            e["category"] = "data"
        elif e["in_ui_context"] and not e["in_data_context"]:
            e["category"] = "ui"
        else:
            e["category"] = "unclassified"
        e["cats"] = dict(e["cats"])

    counts = Counter(e["category"] for e in uniq.values())
    occ = Counter()
    for r in all_recs:
        occ[r["category"]] += 1
    payload = {
        "occurrences": len(all_recs),
        "unique": len(uniq),
        "unique_by_category": dict(counts),
        "occurrences_by_category": dict(occ),
        "strings": sorted(uniq.values(), key=lambda e: e["value"]),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print("occurrences:", len(all_recs), "unique:", len(uniq))
    print("unique by category:", dict(counts))
    print("occurrences by category:", dict(occ))


if __name__ == "__main__":
    main()
