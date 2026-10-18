---
title: Usage
description: Run mddocslint on Markdown files and folders, choose rules, and pick an output format.
---

Before you run the `mddocslint` command, activate the virtual environment in your terminal.

- PowerShell:

  ```
  .venv\Scripts\Activate.ps1
  ```

- Git Bash:

  ```
  source .venv/Scripts/activate
  ```

- macOS and Linux:

  ```
  source .venv/bin/activate
  ```

## Basic command

The basic command to run the `mddocslint` is:

```
mddocslint PATH
```

This command has two parts:

| Part | What it is |
| ---- | ---------- |
| `mddocslint` | The program. It is available as a command once you've [installed](./install.md) the project and activated its virtual environment. |
| `PATH` | The `PATH` argument: path of the file or folder to lint. `PATH` is a required part of the command. You can give it a path to a folder, a single `.md` file, or several of either. |

## Full command

The full command is:

```
mddocslint PATH [PATH ...] [--rules RULES] [--ignore RULES] [--format {text,json}] [-q] [--version] [-h]
```

Everything in square brackets is optional. Options can go before or after the `PATH` component.

| Component | What it does | Default |
| --------- | ------------ | ------- |
| [`PATH`](#path) | Files or folders to lint. Required. | None. |
| [`--rules RULES`](#rules) | Runs only the rules you list. | All three rules. |
| [`--ignore RULES`](#ignore) | Skips the rules you list. | No rules skipped. |
| [`--format`](#format) | Chooses how problems are printed: `text` or `json`. | `text` |
| [`-q`, `--quiet`](#-q-quiet) | Hides the individual problems and prints only the summary line (only for the text format). | Off |
| [`--version`](#version) | Prints the version number and exits. | Off |
| [`-h`, `--help`](#-h-help) | Prints the usage message and exits. | Off |

## PATH

The path to one or more Markdown files or folders to lint. For example:

```
./tests/fixtures/broken-links/missing-file/missing-image.md
```

You can lint multiple files by putting a space between each file.

For example, to lint two files, the command would be:

```
mddocslint doc1.md doc2.md
```

A folder is searched recursively for `.md` files. Folders that start with `.` such as `.git` are ignored. If you pass the same file twice, or a file that is also inside a folder you passed, it's linted once.

mddocslint exits with code 2 if a path doesn't exist, or if a folder contains no Markdown files.

## --rules

Use this component on the command line if you want to run only specific rules.

Options:

- `front-matter`
- `heading-jumps`
- `broken-links`

For what each rule checks, see the [rules reference](./rules.md).

To run more than one rule, separate the names with commas and no spaces.

For example, a command to lint only with the `front-matter` and `broken-links` rules would be:

```
mddocslint PATH --rules front-matter,broken-links
```

If you leave `--rules` out of the command, all three rules run.

## --ignore

Use this component on the command line if you want to skip specific rules and run the rest.

For example, a command to lint without the `broken-links` rule would be:

```
mddocslint PATH --ignore broken-links
```

Options:

- `front-matter`
- `heading-jumps`
- `broken-links`

If you leave `--ignore` out, no rules are skipped.

## Using --rules and --ignore together

You can use `--rules` and `--ignore` together. mddocslint first picks the rules from `--rules`, then removes any that appear in `--ignore`.

If nothing is left to run, the command exits with code 2 and the message `no rules left to run`.

```
mddocslint --rules broken-links --ignore broken-links missing-image.md

usage: mddocslint [-h] [--rules RULES] [--ignore RULES] [--format {text,json}] [-q] [--version] PATH [PATH ...]
mddocslint: error: no rules left to run
```

## --format

Chooses how problems are printed.

Options:

- `text`
- `json`

Any other value is a usage error.

The default is `text`, which shows one line per problem.

```
mddocslint docs docs/guide/setup.md

docs/guide/setup.md:1:1: front-matter[missing] file does not start with a '---' front matter block
docs/guide/setup.md:3:1: heading-jumps[skipped-level] heading jumps from H1 to H3; the next level down is H2
docs/guide/setup.md:5:20: broken-links[missing-file] link target 'guide/missing.md' does not exist
3 problem(s) in 1 file(s)
```

To learn how to read each line, see [Output](./output.md#exit-code-1).

`json` prints the problems as a JSON list.

Each problem is an object with the keys `path`, `line`, `column`, `rule`, `kind`, and `message`:

```
$ mddocslint docs --format json
[
  {
    "path": "docs/guide/setup.md",
    "line": 1,
    "column": 1,
    "rule": "front-matter",
    "kind": "missing",
    "message": "file does not start with a '---' front matter block"
  },
  {
    "path": "docs/guide/setup.md",
    "line": 3,
    "column": 1,
    "rule": "heading-jumps",
    "kind": "skipped-level",
    "message": "heading jumps from H1 to H3; the next level down is H2"
  },
  {
    "path": "docs/guide/setup.md",
    "line": 5,
    "column": 20,
    "rule": "broken-links",
    "kind": "missing-file",
    "message": "link target 'guide/missing.md' does not exist"
  }
]
```

JSON output has no summary line. If there are no problems, it prints an empty list:

```
mddocslint docs/index.md --format json
[]
```

The [exit code](./output.md) is the same in both formats: `1` when problems are found, `0` when none are.

## -q, --quiet

Hides the individual problems. Use it when you only care about the exit code or the total.

Options: none. It's a switch that you either include or leave out.

Default: off, so problems are printed.

With the default `text` format, `--quiet` still prints the summary line:

```
mddocslint docs -q
3 problem(s) in 1 file(s)
```

With `--format json`, `--quiet` prints nothing at all, because the JSON output has no summary line. The exit code is the only result:

```
mddocslint docs --format json -q
$
```

In both cases the exit code is still `1`, because problems were found.

## --version

Prints the installed version number and exits with code 0. mddocslint doesn't lint anything when you use it, so `PATH` isn't needed.

```
mddocslint --version
mddocslint 0.1.0
```

## -h, --help

Prints the usage message, with a short description of each option, and exits with code 0. `PATH` isn't needed here either.

```
mddocslint --help
```
