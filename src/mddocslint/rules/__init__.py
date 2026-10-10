"""Rule registry: rule id -> check function. Each rule lives in its own module."""

from mddocslint.core import Rule
from mddocslint.rules import broken_links, front_matter, heading_jumps

RULES: dict[str, Rule] = {
    front_matter.RULE: front_matter.check,
    heading_jumps.RULE: heading_jumps.check,
    broken_links.RULE: broken_links.check,
}
