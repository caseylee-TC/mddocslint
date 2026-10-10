# mddocslint
A Markdown docs linter, built end-to-end with Claude Code.

It checks a folder of Markdown files for problems:

| Rule | Reports |
| ---- | ------- |
| `front-matter` | missing, unclosed, empty, or invalid YAML front matter |
| `heading-jumps` | headings that skip a level, such as H2 followed by H4 (headings in fenced code are ignored) |

Planned: `broken-links` (internal links to missing files or anchors).

## Install

Requires Python 3.12+. No runtime dependencies.

```
pip install -e ".[dev]"
```

## Usage

```
mddocslint [--select RULES] [--ignore RULES] [--format {text,json}] PATH [PATH ...]
```

```
$ mddocslint docs
docs/guide.md:1:1: front-matter[missing] file does not start with a '---' front matter block
docs/setup.md:3:1: front-matter[invalid-yaml] unquoted value contains ': '; quote the value
2 problem(s) in 2 file(s)
```

- `--select` / `--ignore` take comma-separated rule names.
- Exit codes: `0` clean, `1` problems found, `2` usage error.
