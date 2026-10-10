import pytest

from mddocslint.core import Document, LintContext
from mddocslint.rules import broken_links

RULE = "broken-links"


@pytest.fixture
def target(write_md):
    return write_md("other.md", "# Other\n\n## Section Two\n\n## Intro\n\n## Intro\n")


@pytest.mark.parametrize(
    "link",
    [
        "[x](other.md)",
        "[x](./other.md)",
        "[x](other.md#section-two)",
        "[x](other.md#intro-1)",
        '[x](other.md "Title")',
        "[x](<other.md>)",
        "![img](other.md)",
        "[x](/other.md)",
        "[x](.)",
        "[x](other.md?raw=1)",
        "[x](https://example.com/missing.md)",
        "[x](mailto:someone@example.com)",
        "[x](//cdn.example.com/a.md)",
        "[x](#no-such-heading)",
        "`[x](nowhere.md)`",
        "[x][ref]\n\n[ref]: other.md#section-two",
        "[^1]\n\n[^1]: a footnote, not a link",
    ],
)
def test_valid_links(write_md, run_rule, target, link: str) -> None:
    path = write_md("doc.md", f"# Doc\n\n{link}\n")
    assert run_rule(RULE, path) == []


@pytest.mark.parametrize(
    ("link", "kind"),
    [
        ("[x](nowhere.md)", "missing-file"),
        ("![img](images/nowhere.png)", "missing-file"),
        ("[x](/nowhere.md)", "missing-file"),
        ("[x](nowhere.md#section-two)", "missing-file"),
        ("[x](other.md#no-such-section)", "missing-anchor"),
        ("[x](other.md#Section-Two)", "missing-anchor"),
        ("[x](other.md#intro-2)", "missing-anchor"),
    ],
)
def test_broken_links(write_md, run_rule, target, link: str, kind: str) -> None:
    path = write_md("doc.md", f"# Doc\n\n{link}\n")
    assert run_rule(RULE, path) == [(3, kind)]


def test_relative_paths_resolve_from_the_linking_files_folder(write_md, run_rule) -> None:
    write_md("guide/setup.md", "# Setup\n")
    write_md("index.md", "# Home\n")
    path = write_md(
        "guide/advanced/tips.md",
        "# Tips\n\n[ok](../setup.md) [ok](../../index.md) [bad](../index.md)\n",
    )
    assert run_rule(RULE, path) == [(3, "missing-file")]


def test_root_relative_paths_resolve_from_the_lint_root(write_md, run_rule) -> None:
    write_md("index.md", "# Home\n")
    path = write_md("guide/advanced/tips.md", "# Tips\n\n[ok](/index.md) [bad](/tips.md)\n")
    assert run_rule(RULE, path) == [(3, "missing-file")]


def test_anchor_on_non_markdown_target_is_not_checked(write_md, run_rule, tmp_path) -> None:
    (tmp_path / "data.json").write_text("{}", encoding="utf-8")
    path = write_md("doc.md", "# Doc\n\n[x](data.json#anything)\n")
    assert run_rule(RULE, path) == []


def test_reference_definition_is_checked(write_md, run_rule) -> None:
    path = write_md("doc.md", "# Doc\n\nSee [docs][d].\n\n[d]: ./nowhere.md\n")
    assert run_rule(RULE, path) == [(5, "missing-file")]


def test_links_in_fenced_code_are_ignored(write_md, run_rule) -> None:
    path = write_md("doc.md", "# Doc\n\n```\n[x](nowhere.md)\n```\n")
    assert run_rule(RULE, path) == []


def test_percent_encoded_path(write_md, run_rule) -> None:
    write_md("my file.md", "# Mine\n")
    path = write_md("doc.md", "# Doc\n\n[x](my%20file.md#mine)\n")
    assert run_rule(RULE, path) == []


def test_every_broken_link_on_a_line_is_reported(write_md, run_rule, target) -> None:
    path = write_md("doc.md", "[a](one.md) [b](other.md) [c](other.md#nope)\n")
    assert run_rule(RULE, path) == [(1, "missing-file"), (1, "missing-anchor")]


def test_column_points_at_target(write_md, tmp_path) -> None:
    path = write_md("doc.md", "See [x](nowhere.md).\n")
    [problem] = broken_links.check(Document.load(path), LintContext(tmp_path))
    assert (problem.line, problem.column) == (1, 9)
    assert "nowhere.md" in problem.message
