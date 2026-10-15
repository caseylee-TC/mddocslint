---
title: mddocslint
description: A Markdown docs linter that checks front matter, heading levels, and internal links.
---

mddocslint is a Markdown docs linter, built end-to-end with Claude Code. It checks a folder of Markdown files for three kinds of problems:

| Rule | Reports |
| ---- | ------- |
| `front-matter` | missing, unclosed, empty, or invalid YAML front matter |
| `heading-jumps` | headings that skip a level, such as H2 followed by H4 |
| `broken-links` | internal links and images whose file or `#anchor` doesn't exist |

```
$ mddocslint docs
docs/guide.md:1:1: front-matter[missing] file does not start with a '---' front matter block
docs/setup.md:3:1: front-matter[invalid-yaml] unquoted value contains ': '; quote the value
2 problem(s) in 2 file(s)
```

## Get started

- [Install](./install.md) mddocslint.
- [Run it](./usage.md) on a docs folder.
- See what each check reports in the [rules reference](./rules.md).
- Read the [case study](./case-study.md) about how mddocslint was built.
