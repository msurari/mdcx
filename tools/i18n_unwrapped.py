#!/usr/bin/env python3
"""Report CJK strings passed to UI sinks WITHOUT going through tr().

WHY THIS SHIPS IN THE REPO
    The count of untranslated strings must be reproducible by whoever does the work.
    A number quoted in a brief without the tool that produced it sends the next
    person into archaeology trying to reconstruct the rule, which wastes the run.
    Run this, get a list with file:line, drive it to zero.

METHOD
    AST, not line-matching. A line like `tr("✅ 连接正常！")` contains CJK in its SOURCE KEY
    and is already translated; a line-based grep counts it as untranslated and
    inflates the total (≈285-323 vs the real 48). This walks the tree, finds CJK string
    constants, and excludes any that sit inside a tr() / .translate() call.

ALREADY-TRANSLATED IS NOT THE SAME AS CORRECTLY-TRANSLATED
    A string wrapped in tr() whose key is missing from mdcx/i18n/en.json still
    renders Chinese. This tool does NOT check the dictionary - pair it with a
    key-resolution check.

USAGE
    python3 tools/i18n_unwrapped.py mdcx          # list every finding
    python3 tools/i18n_unwrapped.py mdcx | tail -1   # -> "TOTAL <n>"
    Target: TOTAL 0.
"""
import ast, re, pathlib, collections, sys
CJK=re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]')
UI_METHODS={'setText','setWindowTitle','setToolTip','setPlaceholderText','setInformativeText','setDetailedText','addButton','setTitle','setItemText','addItem','addItems','setStatusTip','showMessage','setLabelText','setHeaderLabels','setTabText','setSpecialValueText','setSuffix','setPrefix','setFormat'}
UI_CTORS={'QAction','QLabel','QPushButton','QCheckBox','QRadioButton','QGroupBox','QMessageBox','QMenu','QListWidgetItem','QTreeWidgetItem','QToolButton'}
STATIC={('QMessageBox','warning'),('QMessageBox','information'),('QMessageBox','critical'),('QMessageBox','question'),('QMessageBox','about'),('QInputDialog','getText'),('QInputDialog','getItem'),('QInputDialog','getInt'),('QFileDialog','getExistingDirectory'),('QFileDialog','getOpenFileName'),('QFileDialog','getSaveFileName'),('QFileDialog','getOpenFileNames')}
LABEL_SIGNALS=re.compile(r'(label_|set_label|pushButton_|set_\w*status|set_javdb|set_\w+_status|label_result|set_main_info)')
out=collections.defaultdict(list)
def raw_cjk(node):
    # CJK constant not inside a tr() call
    res=[]
    def walk(n,in_tr=False):
        if isinstance(n,ast.Call) and getattr(n.func,'id',None)=='tr': in_tr=True
        if isinstance(n,ast.Constant) and isinstance(n.value,str) and CJK.search(n.value) and not in_tr: res.append(n.value)
        for c in ast.iter_child_nodes(n): walk(c,in_tr)
    walk(node); return res
for p in sorted(pathlib.Path(sys.argv[1]).rglob('*.py')):
    if {'views','i18n','crawlers','cmd'} & set(p.parts): continue
    src=p.read_text(encoding='utf-8'); t=ast.parse(src)
    for n in ast.walk(t):
        if not isinstance(n,ast.Call): continue
        f=n.func; kind=None
        if isinstance(f,ast.Attribute):
            if f.attr in UI_METHODS: kind=f.attr
            elif f.attr=='emit' and isinstance(f.value,ast.Attribute) and LABEL_SIGNALS.match(f.value.attr): kind='emit:'+f.value.attr
            elif isinstance(f.value,ast.Name) and (f.value.id,f.attr) in STATIC: kind=f.value.id+'.'+f.attr
        elif isinstance(f,ast.Name) and f.id in UI_CTORS: kind=f.id
        if not kind: continue
        s=[x for a in list(n.args)+[k.value for k in n.keywords] for x in raw_cjk(a)]
        if s: out[str(p)].append((n.lineno,kind,s))
tot=0
for p,items in out.items():
    for l,k,s in sorted(items):
        tot+=1; print(f"{p}:{l} [{k}] "+" | ".join(repr(x)[:70] for x in s))
print("TOTAL",tot)
