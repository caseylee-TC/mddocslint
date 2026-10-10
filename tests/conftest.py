import textwrap
from collections.abc import Callable
from pathlib import Path

import pytest

from mddocslint.core import Document, LintContext
from mddocslint.rules import RULES


@pytest.fixture
def write_md(tmp_path: Path) -> Callable[[str, str], Path]:
    """Write dedented Markdown to tmp_path/relative and return its path."""

    def write(relative: str, text: str) -> Path:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")
        return path

    return write


@pytest.fixture
def run_rule(tmp_path: Path) -> Callable[[str, Path], list[tuple[int, str]]]:
    """Run one rule on one file (lint root = tmp_path) and return (line, kind) pairs."""

    def run(rule: str, path: Path) -> list[tuple[int, str]]:
        problems = RULES[rule](Document.load(path), LintContext(tmp_path))
        return [(problem.line, problem.kind) for problem in problems]

    return run
