"""No display string may reach a Qt widget without going through ``tr()``.

The Chinese source text *is* the dictionary key, so a string that skips ``tr()`` stays
Chinese no matter how complete ``mdcx/i18n/en.json`` is. That failure is invisible in
review (the line looks fine) and invisible at runtime (the widget simply shows Chinese),
which is why it needs a machine check rather than attention.

Three invariants, all meant to be permanent:

* ``tools/i18n_unwrapped.py`` reports ``TOTAL 0`` -- no CJK string reaches a UI sink outside
  ``tr()``;
* every string that *does* go through ``tr()`` has an entry in ``en.json``, because
  ``DictTranslator`` matches the key exactly and silently falls back to the Chinese source
  on a miss -- a wrapped string with no entry renders Chinese just the same;
* every ``tr()`` template's ``{placeholders}`` are supplied by a following ``.format(...)``.
  ``tr()`` does not substitute anything: without the ``.format`` the user literally sees
  ``{link_name}``. ``ruff``'s F841 catches this only when the variable dies with the
  f-string that used to hold it, and is silent when the variable is used elsewhere.

The scan is AST-based on purpose: a line-based grep cannot tell ``tr("✅ 连接正常！")``
(already translated) from ``setText("✅ 连接正常！")``, and over-reports by about 6x.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCANNER = REPO / "tools" / "i18n_unwrapped.py"
EN_JSON = REPO / "mdcx" / "i18n" / "en.json"
PACKAGE = REPO / "mdcx"

PLACEHOLDER = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")


def _run_scanner(target: Path) -> list[str]:
    """Run the shipped scanner over ``target``; return its non-empty output lines."""
    result = subprocess.run(
        [sys.executable, str(SCANNER), str(target)],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"scanner failed:\n{result.stdout}\n{result.stderr}"
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert lines, "scanner printed nothing"
    return lines


def _tr_calls(path: Path, parents: dict[ast.AST, ast.AST]) -> list[tuple[ast.Call, str]]:
    """Every ``tr("literal")`` call in ``path``, with the literal."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    parents.clear()
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "tr" and node.args):
            continue
        arg = node.args[0]
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and arg.value:
            found.append((node, arg.value))
    return found


def _package_files():
    return sorted(path for path in PACKAGE.rglob("*.py") if "i18n" not in path.parts)


def test_no_unwrapped_display_strings():
    """The whole package: every CJK display string must sit inside tr()."""
    lines = _run_scanner(PACKAGE)
    assert lines[-1] == "TOTAL 0", "display strings that bypass tr():\n" + "\n".join(lines)


def test_scanner_still_detects_a_violation(tmp_path: Path):
    """A green scan has to mean 'clean tree', not 'broken scanner'."""
    (tmp_path / "sample.py").write_text(
        'label.setText("\u6b63\u5728\u83b7\u53d6")\n',  # setText("正在获取")
        encoding="utf-8",
    )
    lines = _run_scanner(tmp_path)
    assert lines[-1] == "TOTAL 1", f"scanner did not flag the planted violation: {lines}"


def test_every_tr_key_resolves():
    """A key missing from en.json renders the Chinese source, so the wrap alone is not enough."""
    mapping = json.loads(EN_JSON.read_text(encoding="utf-8"))
    parents: dict[ast.AST, ast.AST] = {}
    keys = [
        (str(path.relative_to(REPO)), node.lineno, literal)
        for path in _package_files()
        for node, literal in _tr_calls(path, parents)
    ]
    assert keys, "no tr() calls found -- the package layout or the helper name changed"
    missing = [entry for entry in keys if entry[2] not in mapping]
    assert not missing, "tr() keys with no en.json entry:\n" + "\n".join(
        f"{path}:{line} {key!r}" for path, line, key in missing
    )


def test_every_template_has_its_placeholders_supplied():
    """``tr()`` does not substitute, so each template needs its own ``.format(...)``."""
    offenders = []
    parents: dict[ast.AST, ast.AST] = {}
    for path in _package_files():
        for node, literal in _tr_calls(path, parents):
            placeholders = PLACEHOLDER.findall(literal)
            if not placeholders:
                continue
            supplied: set[str] = set()
            up = parents.get(node)
            if isinstance(up, ast.Attribute) and up.attr == "format":
                call = parents.get(up)
                if isinstance(call, ast.Call):
                    supplied = {kw.arg for kw in call.keywords if kw.arg}
            missing = sorted({name for name in placeholders if name not in supplied})
            if missing:
                offenders.append(f"{path.relative_to(REPO)}:{node.lineno} missing {missing} in {literal[:40]!r}")
    assert not offenders, "tr() templates whose placeholders are never supplied:\n" + "\n".join(offenders)
