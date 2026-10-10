# mddocslint
A Markdown docs linter, built end-to-end with Claude Code.

It checks a folder of Markdown files for problems:

| Rule | Reports |
| ---- | ------- |
| `front-matter` | missing, unclosed, empty, or invalid YAML front matter |
| `heading-jumps` | headings that skip a level, such as H2 followed by H4 (headings in fenced code are ignored) |
| `broken-links` | internal links and images whose file is missing (`missing-file`) or whose `#anchor` matches no heading in the target `.md` file (`missing-anchor`) |

`broken-links` resolves relative paths such as `../guide/setup.md` against the linking file's folder, and paths starting with `/` against the folder passed on the command line. It skips external URLs, `mailto:` links, anchor-only links such as `#setup`, and anything inside code.

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
