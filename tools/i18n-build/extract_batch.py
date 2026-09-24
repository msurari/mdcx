"""Extract untranslated Chinese strings for a file (or all), with context.

Usage: python extract_batch.py <file.py> [more.py ...]
Writes <out>.json: [{line, text, context, kind}] for review + translation.
"""
import json, pathlib, re, sys

def has_cjk(s): return any('\u4e00' <= c <= '\u9fff' for c in s)

NEVER = {"mdcx/crawlers/guochan.py", "mdcx/crawlers/freejavbt.py", "mdcx/tools/wiki.py"}
STR = re.compile(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'')
UI_CALL = re.compile(r'\.(setText|setToolTip|setTitle|setPlaceholderText|setWindowTitle|addItem|setTabText|setHtml|append|emit)\s*\(|QMessageBox|QInputDialog|QFileDialog')
LOG_CALL = re.compile(r'logging\.|logger\.|\.info\(|\.warning\(|\.error\(|print\(')

def kind(line):
    if UI_CALL.search(line): return "ui"
    if LOG_CALL.search(line): return "log"
    return "other"

def extract(paths):
    out = []
    for rel in paths:
        p = pathlib.Path(rel)
        if not p.exists() or rel in NEVER:
            continue
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, line in enumerate(lines, 1):
            if "tr(" in line or "_translate(" in line:
                continue
            for m in STR.finditer(line):
                s = m.group(1) if m.group(1) is not None else m.group(2)
                if not s or not has_cjk(s):
                    continue
                out.append({"file": rel, "line": i, "text": s,
                            "context": line.strip()[:120], "kind": kind(line)})
    return out

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        args = [str(p) for p in sorted(pathlib.Path("mdcx").rglob("*.py"))]
    items = extract(args)
    # dedupe by text, keeping the first occurrence's context
    seen, uniq = set(), []
    for it in items:
        if it["text"] in seen: continue
        seen.add(it["text"]); uniq.append(it)
    out = pathlib.Path("/tmp/i18n_batch.json")
    out.write_text(json.dumps(uniq, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(items)} occurrences -> {len(uniq)} unique strings -> {out}")
    for it in uniq[:8]:
        print(f"   [{it['kind']:5}] {it['file']}:{it['line']}  {it['text'][:60]}")
