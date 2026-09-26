"""Interface translation layer for MDCx.

Upstream MDCx is Chinese-only and ships no ``QTranslator`` at all: every string in the
Qt Designer interface is wrapped in ``QCoreApplication.translate()`` by ``pyuic6`` but
nothing ever installs a translator, so the Chinese source text is what the user sees.

This module adds the missing half. The mapping lives in ``mdcx/i18n/<lang>.json``
(``{"开始": "Start", ...}``) and is installed on the application *before* the main
window is built, so ``retranslateUi()`` picks it up at construction time.

Design notes
------------
* Dict-backed, so no Qt toolchain (``pylupdate6``/``lrelease``) is needed.
* Unknown strings come back as the original Chinese, so a partial translation degrades
  gracefully instead of showing blank widgets. Note: returning ``""`` does *not* make
  Qt fall back -- measured on PyQt6 6.11 it renders a blank widget (see PROOF.txt);
  returning the source text is what actually works.
* The lookup is by source text and ignores the context argument (``"MDCx"`` /
  ``"Dialog_cut_poster"``). That is deliberate: the interface reuses the same wording
  across contexts, and the mapping is only consulted for strings that already go
  through ``translate()``/``tr()``.
* **Nothing here translates scraped data.** Crawler keywords, tag/genre values, actor
  names, studio/series names and anything written into the ``.nfo`` never pass through
  ``translate()``, so they are untouched.

Usage::

    from mdcx.i18n import install_translator
    install_translator(app)          # after QApplication(), before the main window
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from PyQt6.QtCore import QCoreApplication, QTranslator

if TYPE_CHECKING:
    from PyQt6.QtCore import QObject

logger = logging.getLogger("mdcx.i18n")

TRANSLATIONS_DIR = Path(__file__).resolve().parent
DEFAULT_LANGUAGE = "en"
#: set MDCX_LANG=zh (or any language with no mapping) to keep the upstream interface
LANGUAGE_ENV_VAR = "MDCX_LANG"

#: keeps the installed translator alive -- Qt does not take ownership
_installed: "DictTranslator | None" = None


#: a mapping file is named after a language tag (``en.json``, ``zh-CN.json``); anything
#: else in the directory (``meta.json``) is not a language
LANGUAGE_TAG = re.compile(r"^[A-Za-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})*$")


def available_languages() -> list[str]:
    """Languages with a mapping file in :data:`TRANSLATIONS_DIR`."""
    if not TRANSLATIONS_DIR.is_dir():
        return []
    return sorted(p.stem for p in TRANSLATIONS_DIR.glob("*.json") if LANGUAGE_TAG.match(p.stem))


def language_from_env() -> str:
    """Requested interface language: ``MDCX_LANG`` or :data:`DEFAULT_LANGUAGE`."""
    return os.environ.get(LANGUAGE_ENV_VAR, DEFAULT_LANGUAGE).strip() or DEFAULT_LANGUAGE


def load_translations(language: str = DEFAULT_LANGUAGE) -> dict[str, str]:
    """Load ``mdcx/i18n/<language>.json``.

    Returns an empty mapping (and logs why) when the file is missing or malformed, so a
    broken translation file can never stop the application from starting.
    """
    path = TRANSLATIONS_DIR / f"{language}.json"
    if not path.is_file():
        logger.warning("no translation file for language %r (%s); keeping the original strings", language, path)
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("could not read %s: %s; keeping the original strings", path, exc)
        return {}
    if not isinstance(data, dict):
        logger.warning("%s is not a JSON object; keeping the original strings", path)
        return {}
    # every key is a source string: the mapping file carries no reserved keys
    # (provenance lives in meta.json next to it)
    mapping = {k: v for k, v in data.items() if isinstance(v, str) and v}
    logger.info("loaded %d translations from %s", len(mapping), path)
    return mapping


class DictTranslator(QTranslator):
    """A ``QTranslator`` backed by a plain ``{source: translation}`` dict."""

    def __init__(self, mapping: dict[str, str], language: str = DEFAULT_LANGUAGE, parent: "QObject | None" = None):
        super().__init__(parent)
        self.mapping = mapping
        self.language = language
        self.hits = 0
        self.misses = 0

    def translate(self, context, source_text, disambiguation=None, n=-1) -> str:  # noqa: N802 (Qt API)
        """Return the translation, or the source text when there is none.

        Returning the source text (rather than ``""``) is deliberate: Qt only falls back
        to the source when the returned QString is null, so an empty Python string blanks
        the widget. See PROOF.txt for the measurement.
        """
        value = self.mapping.get(source_text)
        if value is None:
            self.misses += 1
            return source_text
        self.hits += 1
        return value

    @property
    def coverage(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


def install_translator(app: QCoreApplication | None = None, language: str | None = None) -> "DictTranslator | None":
    """Install the dict translator for ``language`` on ``app``.

    Must be called after the ``QApplication`` exists and before the main window is
    constructed. Returns the installed translator, or ``None`` when no mapping is
    available (in which case the application simply stays Chinese).
    """
    global _installed
    app = app or QCoreApplication.instance()
    if app is None:
        logger.warning("no QCoreApplication instance; the interface stays in Chinese")
        return None

    language = language or language_from_env()
    mapping = load_translations(language)
    if not mapping:
        return None

    translator = DictTranslator(mapping, language)
    if app.installTranslator(translator):
        _installed = translator
        logger.info("interface language: %s (%d strings)", language, len(mapping))
        return translator
    logger.warning("Qt refused the %s translator; the interface stays in Chinese", language)
    return None


def uninstall_translator() -> None:
    """Remove a previously installed translator (used by tests)."""
    global _installed
    app = QCoreApplication.instance()
    if _installed is not None and app is not None:
        app.removeTranslator(_installed)
    _installed = None


def current_translator() -> "DictTranslator | None":
    """The installed translator, if any."""
    return _installed


def tr(source_text: str) -> str:
    """Translate a bare string, for call sites that do not live in a ``QObject``.

    Only for interface text: data strings must never be routed through this.
    """
    translated = QCoreApplication.translate("MDCx", source_text)
    return translated or source_text


#: Chinese marker vocabulary that leads dynamic, data-carrying messages (network and
#: parse errors). Those messages are matched against by the retry classifier and by the
#: transport-failure bookkeeping, so the message itself must never be rewritten; only the
#: wording that reaches the screen is swapped here. Longest first.
MESSAGE_MARKERS = (
    "mirror 目标 URL 解析失败",
    "Cloudflare 挑战页且 bypass 失败",
    "mirror 连接错误",
    "请求等待超时",
    "curl-cffi 异常",
    "连接超时",
    "连接错误",
    "请求异常",
    "文本解析失败",
    "JSON解析失败",
    "未知错误",
    "任务已取消",
)


def tr_message(message: str) -> str:
    """UI copy of a dynamic message whose original wording has to stay untouched.

    A whole-message key wins; otherwise the leading marker phrase is translated and the
    technical tail (a URL, a library error) is left exactly as the library produced it.
    """
    if not message:
        return message
    whole = tr(message)
    if whole != message:
        return whole
    for marker in MESSAGE_MARKERS:
        if message.startswith(marker):
            return tr(marker) + message[len(marker):]
    return message


def _main(argv: list[str] | None = None) -> int:
    """``python -m mdcx.i18n [language]`` -- report what a mapping file covers."""
    argv = list(sys.argv[1:] if argv is None else argv)
    language = argv[0] if argv else language_from_env()
    mapping = load_translations(language)
    print(f"language: {language}")
    print(f"file: {TRANSLATIONS_DIR / f'{language}.json'}")
    print(f"entries: {len(mapping)}")
    print(f"available: {', '.join(available_languages()) or '(none)'}")
    return 0 if mapping else 1


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    raise SystemExit(_main())
