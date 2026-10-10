"""Rule registry: rule id -> check function. Each rule lives in its own module."""

from mddocslint.core import Rule
from mddocslint.rules import front_matter

RULES: dict[str, Rule] = {
    front_matter.RULE: front_matter.check,
}
