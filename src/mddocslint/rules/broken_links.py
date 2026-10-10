"""broken-links rule: internal links must point at existing files and existing heading anchors.

Checked: inline links and images [t](target) / ![a](target) and reference definitions
[ref]: target, outside fenced code and inline code. Relative targets resolve against
the linking file's folder; targets starting with '/' resolve against the lint root.

Skipped: external targets with a scheme (https:, mailto:, ...) or starting with '//',
and anchor-only links (#section).
"""

import re
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import unquote

from mddocslint import markdown
from mddocslint.core import Document, LintContext, Problem

RULE = "broken-links"

TARGET = r"(?P<target><[^>]*>|[^\s)]*)"
INLINE_LINK_RE = re.compile(
    r"\]\(\s*" + TARGET + r"""(?:\s+(?:"[^"]*"|'[^']*'|\([^)]*\)))?\s*\)"""
)
REFERENCE_DEF_RE = re.compile(r" {0,3}\[(?!\^)[^\]]+\]:[ \t]*(?P<target><[^>]*>|\S+)")
SCHEME_RE = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*:")


def check(doc: Document, ctx: LintContext) -> list[Problem]:
    problems: list[Problem] = []
    for lineno, line in markdown.iter_content_lines(doc.lines):
        for column, target in iter_targets(markdown.strip_code_spans(line)):
            result = check_target(doc, ctx, target)
            if result:
                kind, message = result
                problems.append(Problem(doc.path, lineno, column, RULE, kind, message))
    return problems


def iter_targets(line: str) -> Iterator[tuple[int, str]]:
    """Yield (1-based column, target) for inline links, images and reference definitions."""
    matches = [*INLINE_LINK_RE.finditer(line)]
    reference = REFERENCE_DEF_RE.match(line)
    if reference:
        matches.append(reference)
    for match in matches:
        target = match["target"]
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        yield match.start("target") + 1, target


def is_internal(target: str) -> bool:
    return bool(target) and not (
        target.startswith(("#", "//")) or SCHEME_RE.match(target)
    )


def check_target(doc: Document, ctx: LintContext, target: str) -> tuple[str, str] | None:
    """Return (kind, message) if an internal target is broken, else None."""
    if not is_internal(target):
        return None
    link_path, _, fragment = target.partition("#")
    link_path = unquote(link_path.partition("?")[0])
    path = resolve(doc, ctx, link_path)
    if not path.exists():
        return "missing-file", f"link target '{target}' does not exist"
    if fragment and path.is_file() and path.suffix.lower() == ".md":
        if unquote(fragment) not in ctx.anchors_for(path):
            return "missing-anchor", f"anchor '#{fragment}' not found in {link_path}"
    return None


def resolve(doc: Document, ctx: LintContext, link_path: str) -> Path:
    if not link_path:
        return doc.path
    if link_path.startswith("/"):
        return ctx.root / link_path.lstrip("/")
    return doc.path.parent / link_path
