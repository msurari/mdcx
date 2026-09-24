"""Truncation must never leave a dangling fragment of a word.

The real-world case: a title ending "...ソープ嬢AVデビュー" clipped at 46 chars
landed one character into "AVデビュー", producing a filename ending in a bare
"A". The clip now walks back to the start of the run instead.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mdcx.core.naming.renderer import _clip_text  # noqa: E402

TITLE = (
    "フードル人気ランキング3ヶ月連続1位!！夏は吉原、冬は海外で接客する"
    "伝説の爆乳爆尻ソープ嬢AVデビュー"
)


def test_does_not_leave_orphan_latin_letter():
    """The exact production case: no bare 'A' left dangling."""
    out = _clip_text(TITLE, 46)
    assert not out.endswith("A"), out
    assert out.endswith("ソープ嬢"), out
    assert "AV" not in out


def test_full_word_is_kept_when_the_cut_lands_after_it():
    """A complete trailing run is not trimmed just for being Latin."""
    assert _clip_text("AVデビュー作品", 2) == "AV"


def test_japanese_only_text_is_untouched():
    assert _clip_text("あいうえおかきくけこ", 5) == "あいうえお"


def test_partial_number_run_is_dropped_whole():
    """'1080' is a fragment of '1080P', so neither survives."""
    assert _clip_text("特集 1080P 高画質", 7) == "特集"


def test_never_returns_empty_when_input_is_non_empty():
    for value, n in [
        ("あいうえお", 1),
        ("ABC", 1),
        ("A", 1),
        ("作品AV", 3),
        ("123456", 2),
        ("x", 1),
    ]:
        assert _clip_text(value, n), f"{value!r} clip {n} emptied"


def test_shorter_than_clip_is_returned_as_is():
    assert _clip_text("短い", 50) == "短い"


def test_zero_length_returns_empty():
    assert _clip_text("なにか", 0) == ""


def test_trailing_punctuation_is_stripped():
    assert _clip_text("作品AVデビュー,", 4) == "作品AV"


def test_default_cap_fits_the_production_title_without_truncating():
    """file_name_max must be generous enough that a normal title survives whole.

    At the old cap of 60 this title was cut mid-word, losing "AVデビュー".
    """
    from mdcx.config.models import Config

    field = Config.model_fields["file_name_max"]
    assert field.default == 100, field.default

    basename_cap = field.default - len(".mp4")
    title_cap = basename_cap - len("【EBOD-875】")
    assert len(_clip_text(TITLE, title_cap)) == len(TITLE)
