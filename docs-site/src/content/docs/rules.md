---
title: Rules reference
description: The checks mddocslint runs and the problem kinds each one reports.
---

The linter checks every `.md` file based on three rules:

1. `front-matter`
2. `heading-jumps`
3. `broken-links`

Each problem it reports names a rule and a kind, as in `front-matter[missing]`. To choose which rules run, use the `--rules` and `--ignore` options (see the [full command](./usage.md#full-command)).

## `front-matter`

This rule checks for missing, unclosed, empty, or invalid basic YAML front matter.

| Kind | Reported when |
| ---- | ------------- |
| `missing` | The file does not start with a `---` line. |
| `unclosed` | The front matter block is never closed with `---`. |
| `empty` | The front matter block has no content. |
| `invalid-yaml` | The block contains invalid YAML, such as an unquoted value that contains `: ` (a colon followed by a space). |

## `heading-jumps`

This rule checks for Markdown style headings (#) that skip a level, such as H2 (##) followed by H4 (####). Headings in fenced code and front matter are ignored.

| Kind | Reported when |
| ---- | ------------- |
| `skipped-level` | A heading skips a level, such as an H2 followed by an H4. |

## `broken-links`

This rule checks for internal links and images whose file is missing (`missing-file`) or whose `#anchor` matches no heading in the target `.md` file (`missing-anchor`).

| Kind | Reported when |
| ---- | ------------- |
| `missing-file` | The linked file doesn't exist. |
| `missing-anchor` | The `#anchor` does not match any heading in the target `.md` file. |

`broken-links` resolves relative paths such as `./guide/setup.md` against the folder of the file that contains the link. It resolves paths that start with `/`, such as `/guide/setup.md`, against the folder you passed as [`PATH`](./usage.md#path). If you pass a single file, it resolves them against the folder that contains that file.

`broken-links` skips external URLs, `mailto:` links, anchor-only links such as `#setup`, and anything inside code.
