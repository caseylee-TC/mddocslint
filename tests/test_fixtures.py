"""Each fixtures/front-matter/<kind>/ file yields exactly one problem of that kind; valid/ yields none."""

from pathlib import Path

import pytest

from mddocslint.core import lint
from mddocslint.rules import RULES

FIXTURES = Path(__file__).parent / "fixtures"
FRONT_MATTER = FIXTURES / "front-matter"
SAMPLE_DOCS = Path(__file__).parent.parent / "sample-docs"

KINDS = {"missing", "unclosed", "empty", "invalid-yaml"}
FIXTURE_FILES = sorted(FRONT_MATTER.glob("*/*.md"))


def expected_kinds(path: Path) -> list[str]:
    return [] if path.parent.name == "valid" else [path.parent.name]


def test_one_subfolder_per_kind_plus_valid() -> None:
    subfolders = {path.name for path in FRONT_MATTER.iterdir() if path.is_dir()}
    assert subfolders == KINDS | {"valid"}
    for name in subfolders:
        assert any((FRONT_MATTER / name).glob("*.md")), f"{name}/ has no fixtures"


@pytest.mark.parametrize(
    "path", FIXTURE_FILES, ids=[f"{p.parent.name}/{p.name}" for p in FIXTURE_FILES]
)
def test_front_matter_fixture(path: Path) -> None:
    problems, _ = lint([path], RULES)
    assert [p.kind for p in problems] == expected_kinds(path)


def test_sample_docs_are_clean() -> None:
    problems, file_count = lint([SAMPLE_DOCS], RULES)
    assert problems == []
    assert file_count == 3
