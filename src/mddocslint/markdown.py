"""Line-based Markdown helpers shared by the rules."""

import re
from collections.abc import Iterator
from dataclasses import dataclass

FENCE_RE = re.compile(r" {0,3}(`{3,}|~{3,})")
ATX_HEADING_RE = re.compile(r" {0,3}(#{1,6})(?:[ \t]+|$)(.*)")
CLOSING_HASHES_RE = re.compile(r"(?:^|[ \t]+)#+[ \t]*$")
CODE_SPAN_RE = re.compile(r"(?<!`)(`+)(?!`).+?(?<!`)\1(?!`)")
LINK_TEXT_RE = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
SLUG_DROP_RE = re.compile(r"[^\w\- ]")


@dataclass(frozen=True)
class Heading:
    line: int
    level: int
    text: str


def has_front_matter(lines: list[str]) -> bool:
    return bool(lines) and lines[0].rstrip() == "---"


def front_matter_close(lines: list[str]) -> int | None:
    """Index of the line closing the front matter block, or None if absent or unclosed."""
    if not has_front_matter(lines):
        return None
    for index in range(1, len(lines)):
        if lines[index].rstrip() in ("---", "..."):
            return index
    return None


def body_start(lines: list[str]) -> int:
    """Index of the first line after a closed front matter block (0 if there is none)."""
    close = front_matter_close(lines)
    return 0 if close is None else close + 1


def iter_content_lines(lines: list[str]) -> Iterator[tuple[int, str]]:
    """Yield (1-based line number, line) outside front matter and fenced code blocks."""
    fence = ""
    for index in range(body_start(lines), len(lines)):
        line = lines[index]
        match = FENCE_RE.match(line)
        if not fence:
            if match:
                fence = match.group(1)
            else:
                yield index + 1, line
        elif match and _closes(fence, match.group(1)) and not line[match.end() :].strip():
            fence = ""


def _closes(opening: str, candidate: str) -> bool:
    """A closing fence uses the opening fence's character and is at least as long."""
    return candidate[0] == opening[0] and len(candidate) >= len(opening)


def iter_headings(lines: list[str]) -> Iterator[Heading]:
    """Yield ATX headings (# to ######) outside front matter and fenced code."""
    for lineno, line in iter_content_lines(lines):
        match = ATX_HEADING_RE.fullmatch(line)
        if match:
            text = CLOSING_HASHES_RE.sub("", match.group(2)).strip()
            yield Heading(lineno, len(match.group(1)), text)


def strip_code_spans(line: str) -> str:
    """Blank out inline code spans, keeping column positions intact."""
    return CODE_SPAN_RE.sub(lambda match: " " * len(match.group()), line)


def slugify(text: str) -> str:
    """GitHub-style heading anchor: lowercase, punctuation dropped, spaces to hyphens."""
    text = LINK_TEXT_RE.sub(r"\1", text)
    text = HTML_TAG_RE.sub("", text)
    text = SLUG_DROP_RE.sub("", text.strip().lower())
    return text.replace(" ", "-")


def anchors(lines: list[str]) -> set[str]:
    """All heading anchors in a document; repeated slugs get -1, -2, ... suffixes."""
    counts: dict[str, int] = {}
    result: set[str] = set()
    for heading in iter_headings(lines):
        base = slugify(heading.text)
        count = counts.get(base, 0)
        counts[base] = count + 1
        result.add(base if count == 0 else f"{base}-{count}")
    return result
