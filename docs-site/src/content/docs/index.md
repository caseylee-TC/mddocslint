---
title: mddocslint
description: A Markdown docs linter that checks front matter, heading levels, and internal links.
---

This is a simple Markdown docs linter, built end-to-end with Claude Code.

By running a command, it lints a Markdown (`.md`) file or a folder of Markdown files for three areas:

1. Front matter
2. Headings
3. Broken links

If mddocslint finds a problem in any of these areas, it reports the file, the line and column where the problem occurs, and the rule that was broken.

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
- Learn how to [read the output](./output.md) and exit codes.
- Set up the [pre-commit hook](./pre-commit.md).
- Read the [case study](./case-study.md) about how mddocslint was built.
