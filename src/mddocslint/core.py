"""Core types and the lint runner shared by the CLI and the rules."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

from mddocslint import markdown


@dataclass(frozen=True, order=True)
class Problem:
    """One lint finding, located at a 1-based line and column."""

    path: Path
    line: int
    column: int
    rule: str
    kind: str
    message: str


@dataclass(frozen=True)
class Document:
    """A Markdown file, loaded once and shared by every rule."""

    path: Path
    lines: list[str]

    @classmethod
    def load(cls, path: Path) -> "Document":
        return cls(path, read_lines(path))


def read_lines(path: Path) -> list[str]:
    # utf-8-sig drops a BOM so a leading '---' still reads as front matter.
    return path.read_text(encoding="utf-8-sig", errors="replace").splitlines()


class LintContext:
    """Per-root state shared by the rules while linting one PATH argument."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self._anchors: dict[Path, set[str]] = {}

    def anchors_for(self, path: Path) -> set[str]:
        """Heading anchors of a Markdown file, parsed once per lint run."""
        key = path.resolve()
        if key not in self._anchors:
            self._anchors[key] = markdown.anchors(read_lines(key))
        return self._anchors[key]


Rule = Callable[[Document, LintContext], list[Problem]]


def discover(target: Path) -> list[Path]:
    """Return the Markdown files under target (or target itself), skipping dot-directories."""
    if target.is_file():
        return [target]
    return sorted(
        path
        for path in target.rglob("*.md")
        if path.is_file()
        and not any(part.startswith(".") for part in path.relative_to(target).parts[:-1])
    )


def lint(targets: Iterable[Path], rules: dict[str, Rule]) -> tuple[list[Problem], int]:
    """Run rules over every Markdown file in targets; return sorted problems and the file count."""
    problems: list[Problem] = []
    seen: set[Path] = set()
    for target in targets:
        context = LintContext(target if target.is_dir() else target.parent)
        for path in discover(target):
            if path.resolve() in seen:
                continue
            seen.add(path.resolve())
            document = Document.load(path)
            for check in rules.values():
                problems.extend(check(document, context))
    return sorted(problems), len(seen)
