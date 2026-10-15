---
title: Install
description: Install mddocslint from source.
---

mddocslint requires Python 3.12 or later and has no runtime dependencies.

## Install from source

1. Clone the repository:

   ```
   git clone https://github.com/caseylee-TC/mddocslint.git
   cd mddocslint
   ```

2. Create and activate a virtualenv:

   - PowerShell:

     ```
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```

   - Git Bash:

     ```
     python -m venv .venv
     source .venv/Scripts/activate
     ```

3. Install the package in editable mode, with the test dependencies:

   ```
   pip install -e ".[dev]"
   ```

4. Check that the `mddocslint` command is available:

   ```
   mddocslint --version
   ```

## Next steps

- [Run mddocslint](./usage.md) on a docs folder.
- [Set up the pre-commit hook](./usage.md#run-mddocslint-before-each-commit) to lint before each commit.
