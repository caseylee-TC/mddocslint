"""heading-jumps rule: a heading may go at most one level deeper than the heading before it.

Only ATX headings (# to ######) count; headings inside fenced code blocks and front
matter are ignored. Going back up any number of levels is fine, and the first
heading may be at any level.
"""

from mddocslint import markdown
from mddocslint.core import Document, LintContext, Problem

RULE = "heading-jumps"


def check(doc: Document, ctx: LintContext) -> list[Problem]:
    problems: list[Problem] = []
    previous: int | None = None
    for heading in markdown.iter_headings(doc.lines):
        if previous is not None and heading.level > previous + 1:
            message = (
                f"heading jumps from H{previous} to H{heading.level}; "
                f"the next level down is H{previous + 1}"
            )
            problems.append(Problem(doc.path, heading.line, 1, RULE, "skipped-level", message))
        previous = heading.level
    return problems
