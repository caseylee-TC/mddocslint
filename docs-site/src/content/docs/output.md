---
title: Output
description: Read mddocslint's problem lines, summary, and exit codes.
---

mddocslint prints its results and then ends with an exit code, a number that tells scripts and CI systems whether the run passed. What you see depends on that code.

To see the exit code of the last command:

- PowerShell:

  ```
  $LASTEXITCODE
  ```

- Git Bash, macOS, and Linux:

  ```
  echo $?
  ```

- Command Prompt:

  ```
  echo %ERRORLEVEL%
  ```

| Exit code | Meaning | Common causes |
| --------- | ------- | ------------- |
| `0` | Clean. The Markdown files passed every rule that ran. | None. |
| `1` | Problems found. At least one rule reported a problem. | The files have problems. Fix them and run the command again. |
| `2` | Usage error. The command couldn't run. | A `PATH` that doesn't exist, a folder with no `.md` files, a misspelled rule name, an invalid `--format` value, an unknown flag, or no `PATH` at all. |

## Exit code 0

mddocslint prints nothing. Silence means success.

```
mddocslint docs/index.md

```

## Exit code 1

Exit code `1` means mddocslint worked and found problems in your docs.

mddocslint prints one line for each problem, then a summary line:

```
mddocslint docs

docs/guide/setup.md:1:1: front-matter[missing] file does not start with a '---' front matter block
docs/guide/setup.md:3:1: heading-jumps[skipped-level] heading jumps from H1 to H3; the next level down is H2
docs/guide/setup.md:5:20: broken-links[missing-file] link target 'guide/missing.md' does not exist

3 problem(s) in 1 file(s)
```

Each problem line follows the same pattern:

```
path:line:column: rule[kind] message
```

| Part | Meaning |
| ---- | ------- |
| `path` | The file that has the problem. |
| `line:column` | Where the problem is in that file. Both numbers start at 1. |
| `rule` | The rule that found it: `front-matter`, `heading-jumps`, or `broken-links`. See the [rules reference](./rules.md). |
| `kind` | The specific type of problem within that rule, such as `missing` or `skipped-level`. |
| `message` | A plain-language description of what's wrong. |

Problems are sorted by file, then by line. The last line is a summary of the total number of problems and the number of files that have them.

For machine-readable output, use `--format json` (see the [full command](./usage.md#full-command)).

## Exit code 2

Exit code `2` means mddocslint couldn't do its job because of the command you typed. Scripts and CI jobs usually treat any non-zero code as a failure, and they can use the number to tell the two cases apart.

The command itself is wrong, so mddocslint doesn't lint anything. It prints the correct syntax and a reason:

```
mddocslint missing-folder
usage: mddocslint [-h] [--rules RULES] [--ignore RULES] [--format {text,json}]
                  [-q] [--version]
                  PATH [PATH ...]
mddocslint: error: path not found: missing-folder
```
