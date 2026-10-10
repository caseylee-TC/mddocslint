"""front-matter rule: each doc must open with a closed, non-empty, valid YAML block.

YAML is checked without a YAML library, so only the subset front matter uses in
practice is understood: block mappings and lists, nested blocks, plain and quoted
scalars, flow collections ([a, b] / {a: b}), block scalars (| and >) and comments.
Other YAML features are accepted where they look like plain values, not reported.
"""

import re
from enum import Enum, auto

from mddocslint import markdown
from mddocslint.core import Document, LintContext, Problem

RULE = "front-matter"

KEY_RE = re.compile(
    r"""(?P<key>"(?:[^"\\]|\\.)*"|'(?:[^']|'')*'|[^\s\-?:,\[\]{}#&*!|>'"%@`](?:[^:#]|(?<=\S)#)*?)"""
    r"""[ \t]*:(?:[ \t]+(?P<value>.*))?"""
)
BLOCK_HEADER_RE = re.compile(r"[|>][1-9+-]{0,2}(?:[ \t]+#.*)?")
COMMENT_RE = re.compile(r"[ \t]+#")


class Scan(Enum):
    OK = auto()
    OPEN = auto()  # an unclosed quote or bracket that may continue on later lines
    BLOCK = auto()  # a | or > block scalar header
    ERROR = auto()


def check(doc: Document, ctx: LintContext) -> list[Problem]:
    lines = doc.lines
    if not markdown.has_front_matter(lines):
        return [_problem(doc, 1, "missing", "file does not start with a '---' front matter block")]
    close = markdown.front_matter_close(lines)
    if close is None:
        return [_problem(doc, 1, "unclosed", "front matter block is never closed with '---'")]
    block = lines[1:close]
    if all(_is_blank_or_comment(line) for line in block):
        return [_problem(doc, 1, "empty", "front matter block is empty")]
    error = validate_yaml(block, first_line=2)
    if error is None:
        return []
    line, message = error
    return [_problem(doc, line, "invalid-yaml", message)]


def _problem(doc: Document, line: int, kind: str, message: str) -> Problem:
    return Problem(doc.path, line, 1, RULE, kind, message)


def validate_yaml(block: list[str], first_line: int) -> tuple[int, str] | None:
    """Return (line number, message) for the first YAML error in block, or None."""
    indents: list[int] = []  # indentation of each open block level, outermost first
    keys: set[str] = set()  # top-level keys, for duplicate detection
    opens_block = False  # the previous entry may be followed by a deeper nested block
    plain_value = False  # the previous entry ended in a plain value that may wrap
    scalar_indent: int | None = None  # inside a | or > block scalar owned by this indent
    pending: tuple[int, str] | None = None  # (line, text) of an unclosed quote or bracket

    for offset, raw in enumerate(block):
        lineno = first_line + offset
        stripped = raw.strip()
        indent = len(raw) - len(raw.lstrip(" "))

        if scalar_indent is not None:
            if not stripped or indent > scalar_indent:
                continue
            scalar_indent = None
        if pending is not None:
            start, text = pending
            text = f"{text} {stripped}"
            status, message = scan_value(text)
            pending = (start, text) if status is Scan.OPEN else None
            if status is Scan.ERROR:
                return start, message
            opens_block = plain_value = False
            continue
        if _is_blank_or_comment(raw):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            return lineno, "tabs are not allowed in YAML indentation"

        content, is_item = _strip_item_markers(stripped)
        match = KEY_RE.fullmatch(content)
        if not indents:
            if is_item or match is None:
                return lineno, "front matter must be a mapping of 'key: value' lines"
            indents.append(indent)
        elif indent > indents[-1]:
            if plain_value and match is None and not is_item:
                continue  # a plain value wrapped onto the next line
            if not opens_block:
                return lineno, "unexpected indentation"
            indents.append(indent)
        elif indent < indents[-1]:
            while indents and indents[-1] > indent:
                indents.pop()
            if not indents or indents[-1] != indent:
                return lineno, "indentation does not match any enclosing level"

        if match:
            value = match["value"] or ""
            if indent == indents[0] and not is_item:
                name = _unquote(match["key"])
                if name in keys:
                    return lineno, f"duplicate key '{name}'"
                keys.add(name)
        elif is_item:
            value = content
        else:
            return lineno, "expected 'key: value'"

        status, message = scan_value(value)
        if status is Scan.ERROR:
            return lineno, message
        if status is Scan.OPEN:
            pending = (lineno, value)
        if status is Scan.BLOCK:
            scalar_indent = indent
        empty = _is_blank_or_comment(value)
        opens_block = empty or (is_item and match is not None)
        plain_value = status is Scan.OK and not empty and value.lstrip()[0] not in "\"'[{"

    if pending is not None:
        start, text = pending
        opener = text.lstrip()[0]
        what = "quoted string" if opener in "\"'" else f"'{opener}'"
        return start, f"unclosed {what}"
    return None


def scan_value(value: str) -> tuple[Scan, str]:
    """Classify a YAML value; the message is set only for Scan.ERROR."""
    value = value.strip()
    if _is_blank_or_comment(value):
        return Scan.OK, ""
    first = value[0]
    if first in "|>":
        if BLOCK_HEADER_RE.fullmatch(value):
            return Scan.BLOCK, ""
        return Scan.ERROR, "invalid block scalar header"
    if first in "@`":
        return Scan.ERROR, f"a value cannot start with '{first}'; quote it"
    if first in "\"'[{":
        end = _closing_index(value)
        if end is None:
            return Scan.OPEN, ""
        if isinstance(end, str):
            return Scan.ERROR, end
        rest = value[end + 1 :]
        if rest.strip() and not COMMENT_RE.match(rest):
            return Scan.ERROR, "unexpected text after closing quote or bracket"
        return Scan.OK, ""
    plain = COMMENT_RE.split(value, maxsplit=1)[0]
    if ": " in plain or plain.endswith(":"):
        return Scan.ERROR, "unquoted value contains ': '; quote the value"
    return Scan.OK, ""


def _closing_index(text: str) -> int | str | None:
    """Index closing text's opening quote or bracket; None if still open, or an error message."""
    closers: list[str] = []
    quote = ""
    previous = ""  # last significant character outside quotes
    index = 0
    while index < len(text):
        char = text[index]
        if quote:
            if quote == '"' and char == "\\":
                index += 2
                continue
            if char == quote:
                if quote == "'" and text[index + 1 : index + 2] == "'":
                    index += 2
                    continue
                quote = ""
                previous = char
                if not closers:
                    return index
        elif char in "\"'" and previous in ("", "[", "{", ",", ":"):
            quote = char
        elif char in "[{":
            closers.append("]" if char == "[" else "}")
            previous = char
        elif char in "]}":
            if not closers or closers.pop() != char:
                return f"mismatched '{char}'"
            if not closers:
                return index
            previous = char
        elif not char.isspace():
            previous = char
        index += 1
    return None


def _strip_item_markers(text: str) -> tuple[str, bool]:
    is_item = False
    while text == "-" or text.startswith("- "):
        text, is_item = text[1:].strip(), True
    return text, is_item


def _is_blank_or_comment(text: str) -> bool:
    stripped = text.strip()
    return not stripped or stripped.startswith("#")


def _unquote(key: str) -> str:
    return key[1:-1] if key[:1] in "\"'" else key
