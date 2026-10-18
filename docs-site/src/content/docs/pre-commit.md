---
title: Pre-commit hook
description: Run mddocslint automatically before each commit with pre-commit.
---

The repo includes a [pre-commit](https://pre-commit.com/) hook for people who contribute to mddocslint itself. If you only want to lint your own docs, you don't need it. See [Add the hook to your own docs project](#add-the-hook-to-your-own-docs-project) if you want a similar hook for your own project.

## What the hook does

Before each commit, the hook runs `mddocslint sample-docs`. This lints `sample-docs/`, the project's demo set of Markdown files, which is kept clean on purpose. If the linter reports any problem, the commit is blocked.

The hook is a safety check for changes to the linter. If an edit to a rule makes it wrongly flag files that are fine, linting `sample-docs` fails and the mistake is caught before it's committed. It also keeps the demo docs themselves clean.

The hook runs only when a commit changes files in `sample-docs/` or `src/mddocslint/`. For any other commit, pre-commit skips it.

## Install the hook

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

## Configuration

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

## What happens when you commit

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

To learn how to read the problem lines, see [Output](./output.md#exit-code-1).

If a commit doesn't change any watched files, the hook is skipped:

```
mddocslint sample-docs................................(no files to check)Skipped
```

## Run the hook without committing

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

## Add the hook to your own docs project

You can use mddocslint in a pre-commit hook in your own project. In your project, [install mddocslint](./install.md) and pre-commit, then add a `.pre-commit-config.yaml` that points at your own docs folder. This example lints a folder called `docs`:

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
