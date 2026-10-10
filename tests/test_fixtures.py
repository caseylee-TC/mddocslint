"""Each Markdown file under fixtures/<rule>/<kind>/ (at any depth), linted on its own with
only that rule, yields exactly one problem of that kind; files under valid/ yield none."""

from pathlib import Path

import pytest

from mddocslint.core import lint
from mddocslint.rules import RULES

FIXTURES = Path(__file__).parent / "fixtures"
SAMPLE_DOCS = Path(__file__).parent.parent / "sample-docs"

KINDS = {
    "front-matter": {"missing", "unclosed", "empty", "invalid-yaml"},
    "heading-jumps": {"skipped-level"},
    "broken-links": {"missing-file", "missing-anchor"},
}
FIXTURE_FILES = sorted(FIXTURES.glob("*/*/**/*.md"))


def test_one_folder_per_rule() -> None:
    assert set(KINDS) == set(RULES)
    assert {path.name for path in FIXTURES.iterdir() if path.is_dir()} == set(RULES)


@pytest.mark.parametrize("rule", sorted(KINDS))
def test_one_subfolder_per_kind_plus_valid(rule: str) -> None:
    subfolders = {path.name for path in (FIXTURES / rule).iterdir() if path.is_dir()}
    assert subfolders == KINDS[rule] | {"valid"}
    for name in subfolders:
        assert any((FIXTURES / rule / name).rglob("*.md")), f"{rule}/{name}/ has no fixtures"


@pytest.mark.parametrize(
    "path",
    FIXTURE_FILES,
    ids=[path.relative_to(FIXTURES).as_posix() for path in FIXTURE_FILES],
)
def test_fixture(path: Path) -> None:
    rule, kind = path.relative_to(FIXTURES).parts[:2]
    problems, _ = lint([path], {rule: RULES[rule]})
    assert [p.kind for p in problems] == ([] if kind == "valid" else [kind])


def test_sample_docs_are_clean() -> None:
    problems, file_count = lint([SAMPLE_DOCS], RULES)
    assert problems == []
    assert file_count == 3
