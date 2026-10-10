---
title: Rules
rules: [front-matter, heading-jumps, broken-links]
---

# Rules

mddocslint runs three rules. Pick some with `--rules` or skip some with `--ignore`;
see [running the linter][running].

![How a doc flows through the rules](../images/rules-flow.svg)

## front-matter

Every page starts with a `---` block of valid YAML, like the one at the top of this page.

## heading-jumps

Headings go down one level at a time. Headings inside fenced code are ignored,
so this example does not count:

```markdown
# Title
#### Skips two levels, but it is only an example
```

## broken-links

Links to other pages, images, and `#anchors` must resolve. Code is not checked,
so `[this](missing.md)` is fine, and so is this block:

```markdown
[Broken on purpose](no-such-page.md)
```

Back to the [contents][home].

[running]: usage.md#running-the-linter
[home]: ../index.md#contents
