"""Regression test: v1 bare-keyword naming templates must convert to Jinja2.

A v1 template such as ``actor/【actor】(release) number`` is neither a known builtin nor braced,
so it used to pass through the migration untouched and was then rendered by v2's Jinja2
environment as literal text — silently renaming every folder and file.
"""

import pytest

from mdcx.config.migrations import _migrate_builtin_naming_templates
from mdcx.core.naming.template import collect_template_fields, render_template

CASES = [
    ("actor/【actor】(release) number",
     "{{ actor }}/【{{ actor }}】({{ release }}) {{ number }}"),
    ("【number】title", "【{{ number }}】{{ title }}"),
    ("actor", "{{ actor }}"),
    ("number title", "{{ number }} {{ title }}"),
]


@pytest.mark.parametrize("v1,expected", CASES)
def test_bare_v1_template_converts(v1, expected):
    data = {"folder_name": v1}
    _migrate_builtin_naming_templates(data)
    assert data["folder_name"] == expected


@pytest.mark.parametrize("v1,_", CASES)
def test_conversion_is_idempotent(v1, _):
    data = {"folder_name": v1}
    _migrate_builtin_naming_templates(data)
    once = data["folder_name"]
    _migrate_builtin_naming_templates(data)
    assert data["folder_name"] == once


def test_migrated_template_reproduces_a_real_name():
    data = {"folder_name": "actor/【actor】(release) number",
            "naming_file": "【number】title"}
    _migrate_builtin_naming_templates(data)
    values = {"actor": "七ツ森りり", "number": "SSNI-854", "release": "2020-08-19",
              "title": "新人NO.1STYLE 芸能人 七ツ森りりAVデビュー"}
    assert render_template(data["folder_name"], values) == "七ツ森りり/【七ツ森りり】(2020-08-19) SSNI-854"
    assert render_template(data["naming_file"], values) == "【SSNI-854】新人NO.1STYLE 芸能人 七ツ森りりAVデビュー"
    assert collect_template_fields(data["folder_name"]) == {"actor", "release", "number"}


def test_v1_marker_flags_map_to_four_booleans():
    """v1's show_4k/show_moword must drive the four v2 flags, not leave them at their defaults."""

    data = {"show_4k": "folder,file,", "show_moword": "file,"}
    migrate_config_data(data)
    assert data["folder_hd"] is True
    assert data["file_hd"] is True
    assert data["folder_moword"] is False   # the one that would otherwise corrupt folder names
    assert data["file_moword"] is True
    assert "show_4k" not in data and "show_moword" not in data


def test_marker_flags_absent_leaves_v2_defaults():
    data = {}
    migrate_config_data(data)
    assert "folder_moword" not in data
