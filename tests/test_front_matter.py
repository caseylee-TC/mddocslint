import pytest

RULE = "front-matter"


def doc(front_matter: str) -> str:
    return f"---\n{front_matter}\n---\n\n# Doc\n"


def test_missing(write_md, run_rule) -> None:
    assert run_rule(RULE, write_md("doc.md", "# No front matter\n")) == [(1, "missing")]


def test_empty_file_is_missing(write_md, run_rule) -> None:
    assert run_rule(RULE, write_md("doc.md", "")) == [(1, "missing")]


def test_unclosed(write_md, run_rule) -> None:
    assert run_rule(RULE, write_md("doc.md", "---\ntitle: x\n\n# Doc\n")) == [(1, "unclosed")]


@pytest.mark.parametrize("body", ["", "\n", "# just a comment"])
def test_empty(write_md, run_rule, body: str) -> None:
    assert run_rule(RULE, write_md("doc.md", doc(body))) == [(1, "empty")]


@pytest.mark.parametrize(
    "front_matter",
    [
        "title: Hello",
        "title: Hello\ntags: [a, b]",
        "title: \"Quoted: with colon\"\nsubtitle: 'It''s quoted'",
        "title: It's fine\nurl: https://example.com\ntime: 12:30",
        "# comment\ntitle: x  # trailing comment",
        "nested:\n  a: 1\n  deeper:\n    b: 2\nnext: 3",
        "tags:\n- a\n- b\nother: x",
        "tags:\n  - a\n  - b",
        "items:\n  - name: a\n    value: 1\n  - name: b\nother: x",
        "description: |\n  Line one: with a colon\n  - not a list\n\n  more\nnext: 1",
        "description: >-\n  folded text\nnext: 1",
        "summary: a long value\n  wrapped onto a second line\ntitle: x",
        "tags: [\n  a,\n  b\n]\ntitle: x",
        'meta: {a: 1, b: [x, "y]"]}',
        '"quoted key": value',
        "empty:\ntitle: x",
        "date: 2026-10-10\ndraft: false",
        "  indented: root\n  is: fine",
    ],
)
def test_valid_yaml(write_md, run_rule, front_matter: str) -> None:
    assert run_rule(RULE, write_md("doc.md", doc(front_matter))) == []


@pytest.mark.parametrize(
    ("front_matter", "line"),
    [
        ("title My Doc", 2),
        ("title:no-space", 2),
        ("- a\n- b", 2),
        ("title: x\nnot a key", 3),
        ('title: "unclosed', 2),
        ('title: x\nsubtitle: "unclosed\ndate: 2026', 3),
        ("tags: [a, b", 2),
        ("tags: [a, b}", 2),
        ("title: Foo: Bar", 2),
        ("title: Note:", 2),
        ('title: "a" extra', 2),
        ("handle: @me", 2),
        ("\ttitle: x", 2),
        ("tags:\n\t- a", 3),
        ("title: a\ntitle: b", 3),
        ("title: a\n  bad: indent", 3),
        ("nested:\n    a: 1\n  b: 2", 4),
        ("text: |x\nnext: 1", 2),
    ],
)
def test_invalid_yaml(write_md, run_rule, front_matter: str, line: int) -> None:
    assert run_rule(RULE, write_md("doc.md", doc(front_matter))) == [(line, "invalid-yaml")]


def test_bom_is_ignored(tmp_path, run_rule) -> None:
    path = tmp_path / "doc.md"
    path.write_text("﻿---\ntitle: x\n---\n# Doc\n", encoding="utf-8")
    assert run_rule(RULE, path) == []
