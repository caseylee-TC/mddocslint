import pytest

from mddocslint import markdown


def test_front_matter_must_start_on_line_1() -> None:
    assert markdown.has_front_matter(["---", "title: x", "---"])
    assert not markdown.has_front_matter(["", "---", "title: x", "---"])
    assert not markdown.has_front_matter([])


def test_front_matter_close() -> None:
    assert markdown.front_matter_close(["---", "title: x", "---", "# Doc"]) == 2


def test_dots_close_front_matter() -> None:
    assert markdown.front_matter_close(["---", "title: x", "..."]) == 2


def test_unclosed_front_matter() -> None:
    assert markdown.front_matter_close(["---", "title: x"]) is None
    assert markdown.body_start(["---", "title: x"]) == 0


def test_body_starts_after_front_matter() -> None:
    assert markdown.body_start(["---", "title: x", "---", "# Doc"]) == 3
    assert markdown.body_start(["# Doc"]) == 0


def test_content_lines_skip_front_matter_and_fences() -> None:
    lines = ["---", "title: x", "---", "a", "```", "b", "~~~", "c", "```", "d", "~~~~", "e"]
    assert list(markdown.iter_content_lines(lines)) == [(4, "a"), (10, "d")]


def test_fence_closes_only_with_same_char_and_enough_length() -> None:
    lines = ["````", "```", "inside", "````", "outside"]
    assert list(markdown.iter_content_lines(lines)) == [(5, "outside")]


def test_fence_close_line_must_be_bare() -> None:
    lines = ["```", "``` python", "inside", "```", "outside"]
    assert list(markdown.iter_content_lines(lines)) == [(5, "outside")]


def test_headings_parse_levels_and_text() -> None:
    lines = ["# One #", "## Two", "#NoSpace", "####### Seven", "   ### Indented", "    ## Code", "#"]
    assert [(h.line, h.level, h.text) for h in markdown.iter_headings(lines)] == [
        (1, 1, "One"),
        (2, 2, "Two"),
        (5, 3, "Indented"),
        (7, 1, ""),
    ]


def test_heading_keeps_hash_inside_text() -> None:
    [heading] = markdown.iter_headings(["## C# tips"])
    assert heading.text == "C# tips"


@pytest.mark.parametrize(
    ("text", "slug"),
    [
        ("Hello World", "hello-world"),
        ("What's new?", "whats-new"),
        ("Use `foo()` here", "use-foo-here"),
        ("[Linked](other.md) title", "linked-title"),
        ("snake_case and kebab-case", "snake_case-and-kebab-case"),
        ("Déjà vu", "déjà-vu"),
    ],
)
def test_slugify(text: str, slug: str) -> None:
    assert markdown.slugify(text) == slug


def test_anchors_number_duplicate_headings() -> None:
    lines = ["# Intro", "## Intro", "## Intro", "## Other"]
    assert markdown.anchors(lines) == {"intro", "intro-1", "intro-2", "other"}


def test_anchors_include_smart_dash_slugs() -> None:
    lines = ["## --format", "## -q, --quiet", "## --format"]
    assert markdown.anchors(lines) == {
        "--format", "--format-1", "format", "format-1", "-q---quiet", "-q-quiet",
    }


def test_anchors_ignore_headings_in_fences() -> None:
    assert markdown.anchors(["# Real", "```", "# Fake", "```"]) == {"real"}


def test_strip_code_spans_keeps_columns() -> None:
    line = "see `[x](y.md)` and ``a ` b``"
    stripped = markdown.strip_code_spans(line)
    assert len(stripped) == len(line)
    assert "[x]" not in stripped
    assert stripped.startswith("see ")
