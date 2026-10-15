---
title: Rules reference
description: The checks mddocslint runs and the problem kinds each one reports.
---

mddocslint has three rules. Each problem it reports names a rule and a kind, as in `front-matter[missing]`. To choose which rules run, use `--rules` and `--ignore` (see [Usage](./usage.md#options)).

## front-matter

Each file must start with a YAML front matter block that is closed, not empty, and valid.

| Kind | Reported when |
| ---- | ------------- |
| `missing` | The file doesn't start with a `---` line. |
| `unclosed` | The front matter block is never closed with `---`. |
| `empty` | The front matter block has no content. |
| `invalid-yaml` | The block contains invalid YAML, such as an unquoted value that contains `: `. |

## heading-jumps

A heading can be at most one level deeper than the heading before it. Headings inside fenced code blocks are ignored.

| Kind | Reported when |
| ---- | ------------- |
| `skipped-level` | A heading skips a level, such as an H2 followed by an H4. |

## broken-links

Internal links and images must point to files that exist, and their `#anchor` fragments must match a heading in the target `.md` file.

| Kind | Reported when |
| ---- | ------------- |
| `missing-file` | The linked file doesn't exist. |
| `missing-anchor` | The `#anchor` doesn't match any heading in the target `.md` file. |

`broken-links` resolves paths this way:

- Relative paths, such as `../guide/setup.md`, resolve against the linking file's folder.
- Paths starting with `/` resolve against the folder passed on the command line.

It skips external URLs, `mailto:` links, anchor-only links such as `#setup`, and anything inside code.
