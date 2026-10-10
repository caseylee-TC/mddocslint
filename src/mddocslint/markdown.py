"""Line-based Markdown helpers shared by the rules."""


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
