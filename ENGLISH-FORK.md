# English interface fork

This is `msurari/mdcx`, a fork of [Hazard804/mdcx](https://github.com/Hazard804/mdcx) (release
**220260517**). It adds an **English interface** for self-hosted use. Everything else is upstream.

## What this fork adds

| path | what it is |
|---|---|
| `mdcx/i18n/__init__.py` | `DictTranslator` — a `QTranslator` subclass backed by a JSON map |
| `mdcx/i18n/en.json` | the translation map: `{"<Chinese source>": "<English>"}`, 889 entries |
| `mdcx/i18n/meta.json` | provenance for the map (upstream commit, counts, batch files) |
| `main.py` | installs the translator **before** the main window is constructed |
| `tools/i18n-build/` | the reproducible extraction / classification / translation pipeline |

No upstream source string was edited. The generated view code already calls
`QCoreApplication.translate`, so the interface is translated by the layer alone — which keeps merges from
upstream clean.

## Behaviour

- Unknown string → the translator returns the **source text**, so a partial map degrades to Chinese
  rather than to blank widgets. (This is not the obvious implementation — see below.)
- `MDCX_LANG` selects the map; unset defaults to English.
- The map is keyed on the **exact** source string, **including surrounding whitespace**. Several widget
  strings carry padding (`" 设置"`, `" 命名 "`), so a lookup for the bare word will miss. Always key on the
  string as it appears in the `.ui`.

## Two PyQt6 6.11 findings — do not undo these

1. **Returning `""` from `QTranslator.translate` does not fall back.** The widget goes **blank**, and
   every non-Chinese source (such as the context name `MDCx`) would be blanked too. The translator returns
   the source text instead, which Qt renders identically to a real fallback.
2. **A `_`-prefixed metadata key in the map swallowed a real source string.** An early loader skipped
   every key starting with `_` and silently dropped the `.ui` string `_ 下划线`. `en.json` is a pure flat
   map; provenance lives in `meta.json`.

Both were found only by resolving strings **through Qt** rather than reading the JSON — keep
`tools/i18n-build/proof_i18n.py` as the acceptance test.

## Coverage (phase 1)

- `.ui` strings: **658 / 659** unique (**816 / 817** occurrences). The single deferral is the embedded
  help manual (one `QTextBrowser` `html` property, ~38 KB), left in Chinese deliberately.
- Settings vocabulary (`config/models.py`, `config/enums.py`): 231 labels added to the map.
  **Caveat: nothing reads them yet** — `FieldInfo.title` has no call site and the `names()` classmethods
  are dead code. The settings screen is hand-built in `MDCx.ui`, so its visible labels come from the `.ui`
  batch. They are in the map for the vocabulary, not for a runtime effect.
- **Phase 2, not done:** ~2,159 Chinese strings in `.py` that are not routed through Qt today. They need
  `mdcx.i18n.tr()` calls at their call sites. 378 of them could not be safely classified as interface and
  were left in Chinese rather than guessed at.

## Hard rule — never translate these

`mdcx/crawlers/*`, `mdcx/tools/wiki.py`, data-source names, tag/genre values, actor names, studio and
series names, and anything matched against a website or written into the `.nfo` as data. These are site
keywords and content, not interface. Translating them **silently breaks scraping**. Eight values in
`en.json` deliberately still contain Han characters because they quote keyword literals the app matches.

## Regenerating the map

```bash
cd tools/i18n-build
python scan_ui.py          # both .ui files -> ui_strings.json
python build_canon.py      # de-duplicate, document order -> canon.json
python scan_py.py          # .py literals by AST context
python classify_py.py      # ui / data / unclassified
python extract_settings_labels.py
python build_en_json.py    # joins the tr_*.py batches -> mdcx/i18n/en.json
python proof_i18n.py       # acceptance test -> PROOF.txt
```
The `tr_ui_a..e.py` / `tr_settings.py` batches are keyed by **canon index**, so no Chinese source string is
ever re-typed by hand.

## Image build

Upstream ships no Dockerfile (only `scripts/build.py`, a PyInstaller script). The image is built by the
`northsea4/mdcx-docker` project. A Dockerfile for this fork is **not yet in the tree** — until it is, the
fork is not yet deployable. Tracked as the next step.
