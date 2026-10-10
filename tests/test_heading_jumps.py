import pytest

RULE = "heading-jumps"


@pytest.mark.parametrize(
    "text",
    [
        "# A\n## B\n### C\n## D\n# E\n",
        "### Starts deep\n#### Then one more\n",
        "# A\n```\n### Inside a backtick fence\n```\n## B\n",
        "# A\n~~~\n### Inside a tilde fence\n~~~\n## B\n",
        "# A\n````\n```\n### Inside a longer fence\n```\n````\n## B\n",
        "# A\n####no-space-is-not-a-heading\n## B\n",
        "# A\n\n    ### Indented code\n\n## B\n",
        "",
    ],
)
def test_no_jumps(write_md, run_rule, text: str) -> None:
    assert run_rule(RULE, write_md("doc.md", text)) == []


@pytest.mark.parametrize(
    ("text", "line"),
    [
        ("# A\n\n### C\n", 3),
        ("# A\n## B\n#### D\n", 3),
        ("# A\n## B\n### C\n# D\n### E\n", 5),
        ("# A\n```\n## In a fence\n```\n### C\n", 5),
        ("# A\n## B #\n#### D ####\n", 3),
    ],
)
def test_jump(write_md, run_rule, text: str, line: int) -> None:
    assert run_rule(RULE, write_md("doc.md", text)) == [(line, "skipped-level")]


def test_each_jump_is_reported(write_md, run_rule) -> None:
    path = write_md("doc.md", "# A\n### C\n# D\n#### E\n")
    assert run_rule(RULE, path) == [(2, "skipped-level"), (4, "skipped-level")]


def test_unclosed_fence_hides_the_rest(write_md, run_rule) -> None:
    path = write_md("doc.md", "# A\n```\n### never seen\n")
    assert run_rule(RULE, path) == []


def test_front_matter_is_not_counted(write_md, run_rule) -> None:
    path = write_md("doc.md", "---\n# yaml comment\ntitle: x\n---\n# A\n### C\n")
    assert run_rule(RULE, path) == [(6, "skipped-level")]


def test_message_names_both_levels(write_md, tmp_path) -> None:
    from mddocslint.core import Document, LintContext
    from mddocslint.rules import heading_jumps

    path = write_md("doc.md", "## B\n#### D\n")
    [problem] = heading_jumps.check(Document.load(path), LintContext(tmp_path))
    assert "H2 to H4" in problem.message
