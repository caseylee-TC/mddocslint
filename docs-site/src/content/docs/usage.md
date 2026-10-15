---
title: Usage
description: Run mddocslint on Markdown files and folders, choose rules, and read the output.
---

```
mddocslint [--rules RULES] [--ignore RULES] [--format {text,json}] [-q] PATH [PATH ...]
```

Pass one or more Markdown files or folders. mddocslint runs every rule on every file it finds:

```
$ mddocslint docs
docs/guide.md:1:1: front-matter[missing] file does not start with a '---' front matter block
docs/setup.md:3:1: front-matter[invalid-yaml] unquoted value contains ': '; quote the value
2 problem(s) in 2 file(s)
```

Each problem line has the form `path:line:column: rule[kind] message`. For the rules and kinds, see the [rules reference](./rules.md).

## Options

| Option | Description |
| ------ | ----------- |
| `--rules RULES` | Run only these rules, as a comma-separated list, such as `--rules front-matter,broken-links`. |
| `--ignore RULES` | Skip these rules, as a comma-separated list. |
| `--format {text,json}` | Output format. The default is `text`. |
| `-q`, `--quiet` | Hide the per-problem lines, but keep the summary line and the exit code. |
| `--version` | Print the version and exit. |

## Exit codes

| Code | Meaning |
| ---- | ------- |
| `0` | No problems found. |
| `1` | Problems found. |
| `2` | Usage error, such as an unknown rule name. |

## Run mddocslint before each commit

The repository includes a [pre-commit](https://pre-commit.com/) hook that runs `mddocslint sample-docs` before each commit, and blocks the commit if it finds problems. It runs only when a commit changes files in `sample-docs/` or `src/mddocslint/`.

pre-commit isn't one of this project's dependencies, so install it separately. Then install the hook into your clone:

```
pip install pre-commit
pre-commit install
```

The hook runs the `mddocslint` command from your environment, so activate the virtualenv before you commit:

- PowerShell: `.venv\Scripts\Activate.ps1`
- Git Bash: `source .venv/Scripts/activate`

If you commit from an editor or Git client, make sure it uses the activated virtualenv, or the hook fails with "Executable `mddocslint` not found".

To run the hook without committing:

```
pre-commit run mddocslint --all-files
```
