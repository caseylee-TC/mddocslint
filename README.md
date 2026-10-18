# mddocslint
This is a simple Markdown docs linter, built end-to-end with Claude Code.

By running a command, it lints a Markdown (`.md`) file or a folder of Markdown files for three areas:

1. Front matter
2. Headings
3. Broken links

If mddocslint finds a problem in any of these areas, it reports the file, the line and column where the problem occurs, and the rule that was broken.


## Install

### Prerequisite
- Requires Python 3.12+
- [Git](https://git-scm.com/downloads) 

mddocslint has no runtime dependencies.

### Installation steps

1. Clone the repository and move into it:

   ```
   git clone https://github.com/caseylee-TC/mddocslint.git
   cd mddocslint
   ```

2. Create a virtual environment. This keeps mddocslint separate from your other Python projects:

   ```
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - PowerShell
   ```
   .venv\Scripts\Activate.ps1
   ```
   - Git Bash
   ```
   source .venv/Scripts/activate
   ```
   - macOS and Linux:
   ```
   source .venv/bin/activate
   ```

   When it's active, your prompt starts with `(.venv)`. You must activate it again in every new terminal before you use `mddocslint`.

4. Install mddocslint:
   ```
   python -m pip install .
   ```

   > [!NOTE]
   > If you plan to change the code and run tests, install in editable mode with the `dev` extras (pytest):
   >   ```
   >  python -m pip install -e ".[dev]"
   > ```
   >
   >Editable mode links the installed command to the files in `src/`, so your edits take effect right away. Run the tests with `pytest`.
5. Check that it is installed:
   ```
   mddocslint --help
   ```
   If you see the usage message, you're ready to go. If your shell says it can't find `mddocslint`, the virtual environment isn't active. Repeat step 3.

To update mddocslint later, run `git pull` and then `python -m pip install .` again. A regular install is a copy, so it doesn't pick up changes until you reinstall.

## Rules
The linter checks every `.md` file based on three rules:
1. `front-matter`
2. `heading-jumps`
3. `broken-links`

### `front-matter`
This rule checks for missing, unclosed, empty, or invalid basic YAML front matter.

### `heading-jumps`
This rule checks for Markdown style headings (#) that skip a level, such as H2 (##) followed by H4 (####). Headings in fenced code and front matter are ignored. 

### `broken-links`
This rule checks for internal links and images whose file is missing (`missing-file`) or whose `#anchor` matches no heading in the target `.md` file (`missing-anchor`).

`broken-links` resolves relative paths such as `../guide/setup.md` against the folder of the file that contains the link. It resolves paths that start with `/`, such as `/guide/setup.md`, against the folder you passed as `PATH`. If you pass a single file, it resolves them against the folder that contains that file.

`broken-links` skips external URLs, `mailto:` links, anchor-only links such as `#setup`, and anything inside code.

## Usage
Before you run the `mddocslint` command, activate the virtual environment in your terminal.

  - PowerShell
  ```
  .venv\Scripts\Activate.ps1
  ```
  - Git Bash
  ```
  source .venv/Scripts/activate
  ```
  - macOS and Linux:
  ```
  source .venv/bin/activate
  ```
### Basic command
The basic command to run the `mddocslint` is:

```
mddocslint PATH
```

This command has two parts:

| Part | What it is |
| ---- | ---------- |
| `mddocslint` | The program. It is available as a command once you've installed the project and activated its virtual environment. |
| `PATH` | The `PATH` argument: path of the file or folder to lint. `PATH` is a required part of the command. You can give it a path to a folder, a single `.md` file, or several of either. |
### Full command
The full command is:

```
mddocslint PATH [PATH ...] [--rules RULES] [--ignore RULES] [--format {text,json}] [-q] [--version] [-h] 
```

Everything in square brackets is optional. Options can go before or after the `PATH` component.

| Component | What it does | Default |
| --------- | ------------ | ------- |
| `PATH` | Files or folders to lint. Required. | None. |
| `--rules RULES` | Runs only the rules you list. | All three rules. |
| `--ignore RULES` | Skips the rules you list. | No rules skipped. |
| `--format` | Chooses how problems are printed: `text` or `json`. | `text` |
| `-q`, `--quiet` | Hides the individual problems and prints only the summary line (only for the text format). | Off |
| `--version` | Prints the version number and exits. | Off |
| `-h`, `--help` | Prints the usage message and exits. | Off |

### PATH

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

### --rules

Use this component on the command line if you want to run only specific rules.

Options: 
- `front-matter`
- `heading-jumps`
- `broken-links`

To run more than one rule, separate the names with commas and no spaces.

For example, a command to lint only with the `front-matter` and `broken-links` rules would be:

```
mddocslint PATH --rules front-matter,broken-links
```

If you leave `--rules` out of the command, all three rules run.

### --ignore

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

### Using --rules and --ignore together

You can use `--rules` and `--ignore` together. mddocslint first picks the rules from `--rules`, then removes any that appear in `--ignore`. 

If nothing is left to run, the command exits with code 2 and the message `no rules left to run`.

```
mddocslint --rules broken-links --ignore broken-links missing-image.md

usage: mddocslint [-h] [--rules RULES] [--ignore RULES] [--format {text,json}] [-q] [--version] PATH [PATH ...]
mddocslint: error: no rules left to run
```

### --format

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

The exit code is the same in both formats: `1` when problems are found, `0` when none are.

### -q, --quiet

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

### --version

Prints the installed version number and exits with code 0. mddocslint doesn't lint anything when you use it, so `PATH` isn't needed.

```
mddocslint --version
mddocslint 0.1.0
```

### -h, --help

Prints the usage message, with a short description of each option, and exits with code 0. `PATH` isn't needed here either.

```
mddocslint --help
```

## Output

mddocslint prints its results and then ends with an exit code, a number that tells scripts and CI systems whether the run passed. What you see depends on that code. 

To see the exit code of the last command:

- PowerShell: 
   ```
   LASTEXITCODE
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

### Exit code 0
mddocslint prints nothing. Silence means success.

```
mddocslint docs/index.md

```

### Exit code 1
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
| `rule` | The rule that found it: `front-matter`, `heading-jumps`, or `broken-links`. |
| `kind` | The specific type of problem within that rule, such as `missing` or `skipped-level`. |
| `message` | A plain-language description of what's wrong. |

Problems are sorted by file, then by line. The last line is a summary of the total number of problems and the number of files that have them.

### Exit code 2

Exit code `2` means mddocslint couldn't do its job because of the command you typed. Scripts and CI jobs usually treat any non-zero code as a failure, and they can use the number to tell the two cases apart.

The command itself is wrong, so mddocslint doesn't lint anything. It prints the correct syntax and a reason:

```
mddocslint missing-folder
usage: mddocslint [-h] [--rules RULES] [--ignore RULES] [--format {text,json}]
                  [-q] [--version]
                  PATH [PATH ...]
mddocslint: error: path not found: missing-folder
```

## Pre-commit hook

The repo includes a [pre-commit](https://pre-commit.com/) hook for people who contribute to mddocslint itself. If you only want to lint your own docs, you don't need it. See [Add the hook to your own docs project](#add-the-hook-to-your-own-docs-project) if you want a similar hook for your own project.

### What the hook does

Before each commit, the hook runs `mddocslint sample-docs`. This lints `sample-docs/`, the project's demo set of Markdown files, which is kept clean on purpose. If the linter reports any problem, the commit is blocked.

The hook is a safety check for changes to the linter. If an edit to a rule makes it wrongly flag files that are fine, linting `sample-docs` fails and the mistake is caught before it's committed. It also keeps the demo docs themselves clean.

The hook runs only when a commit changes files in `sample-docs/` or `src/mddocslint/`. For any other commit, pre-commit skips it.

### Install the hook

pre-commit isn't one of this project's dependencies, so install it separately. Then install the hook into your clone:

```
pip install pre-commit
pre-commit install
```

Git hooks aren't shared through the repository, so run `pre-commit install` once in every clone.

The hook runs the `mddocslint` command from your environment, so activate the virtual environment before you commit:

- PowerShell: `.venv\Scripts\Activate.ps1`
- Git Bash: `source .venv/Scripts/activate`

If you commit from an editor or Git client, make sure it uses the activated virtual environment, or the hook fails with "Executable `mddocslint` not found".

### Configuration

The hook is defined in `.pre-commit-config.yaml` at the root of the repo:

```yaml
repos:
  - repo: local
    hooks:
      - id: mddocslint
        name: mddocslint sample-docs
        entry: mddocslint sample-docs
        language: system
        pass_filenames: false
        files: ^(sample-docs|src/mddocslint)/
```

| Setting | What it does |
| ------- | ------------ |
| `repo: local` | The hook is defined in this file. pre-commit doesn't download it from another repository. |
| `id` | The hook's identifier, used in commands such as `pre-commit run mddocslint`. |
| `name` | The label shown in the output when the hook runs. |
| `entry` | The command to run. |
| `language: system` | Use a program that's already installed in your environment, instead of having pre-commit build its own. This is why the virtual environment must be active. |
| `pass_filenames: false` | Don't add the names of the changed files to the command, so it always lints the whole folder. |
| `files` | A pattern for file paths. The hook runs only if at least one file in the commit matches it. |

### What happens when you commit

If the hook passes, the commit goes through:

```
$ git commit -m "Update usage guide"
mddocslint sample-docs...................................................Passed
```

If the hook finds problems, it prints them and the commit is blocked. Fix the problems, stage the files again with `git add`, and commit again:

```
$ git commit -m "Add new page"
mddocslint sample-docs...................................................Failed
- hook id: mddocslint
- exit code: 1

sample-docs/guide/new-page.md:1:1: front-matter[missing] file does not start with a '---' front matter block
1 problem(s) in 1 file(s)
```

If a commit doesn't change any watched files, the hook is skipped:

```
mddocslint sample-docs................................(no files to check)Skipped
```

### Run the hook without committing

To run the hook on all files:

```
pre-commit run mddocslint --all-files
```

To run it only on the files you've staged, leave out `--all-files`.

To skip the hook for a single commit, add `--no-verify`:

```
git commit --no-verify -m "Your message"
```

To remove the hook from your clone, run `pre-commit uninstall`.

### Add the hook to your own docs project

You can use mddocslint in a pre-commit hook in your own project. In your project, install mddocslint and pre-commit, then add a `.pre-commit-config.yaml` that points at your own docs folder. This example lints a folder called `docs`:

```yaml
repos:
  - repo: local
    hooks:
      - id: mddocslint
        name: mddocslint docs
        entry: mddocslint docs
        language: system
        pass_filenames: false
        files: ^docs/
```

Change `entry` and `files` together. `entry` sets the folder that's linted, and `files` sets which changes trigger the hook. To skip a rule, add the flag to `entry`, for example `mddocslint docs --ignore broken-links`. Then run `pre-commit install` in your project.
