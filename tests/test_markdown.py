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
